#!/usr/bin/env python
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler

from train_c_lstm import CLSTMClassifier, resolve_device, save_confusion_matrix, set_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an improved local version of the C-LSTM classifier.")
    parser.add_argument("--data", required=True, help="Path to the prepared .npz packet dataset.")
    parser.add_argument("--output-dir", required=True, help="Directory for training outputs.")
    parser.add_argument("--batch-size", type=int, default=64, help="Mini-batch size.")
    parser.add_argument("--epochs", type=int, default=15, help="Maximum number of epochs.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="AdamW learning rate.")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="AdamW weight decay.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Hold-out test split ratio.")
    parser.add_argument(
        "--val-size",
        type=float,
        default=0.1,
        help="Validation split ratio inside the training split.",
    )
    parser.add_argument("--dropout", type=float, default=0.15, help="Dropout used inside the C-LSTM classifier.")
    parser.add_argument("--scheduler-patience", type=int, default=2, help="ReduceLROnPlateau patience.")
    parser.add_argument("--early-stop-patience", type=int, default=5, help="Early stopping patience.")
    parser.add_argument("--min-learning-rate", type=float, default=1e-5, help="Scheduler lower bound.")
    parser.add_argument("--grad-clip", type=float, default=5.0, help="Gradient clipping threshold.")
    parser.add_argument("--label-smoothing", type=float, default=0.05, help="CrossEntropy label smoothing.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda.")
    return parser.parse_args()


def build_eval_loader(x: np.ndarray, y: np.ndarray, indices: np.ndarray, batch_size: int) -> DataLoader:
    dataset = TensorDataset(torch.from_numpy(x[indices]), torch.from_numpy(y[indices]))
    return DataLoader(dataset, batch_size=batch_size, shuffle=False)


def build_train_loader(
    x: np.ndarray,
    y: np.ndarray,
    indices: np.ndarray,
    batch_size: int,
) -> DataLoader:
    dataset = TensorDataset(torch.from_numpy(x[indices]), torch.from_numpy(y[indices]))
    y_subset = y[indices]
    class_counts = np.bincount(y_subset)
    class_weights = class_counts.sum() / (len(class_counts) * np.maximum(class_counts, 1))
    sample_weights = class_weights[y_subset]
    sampler = WeightedRandomSampler(
        weights=torch.as_tensor(sample_weights, dtype=torch.double),
        num_samples=len(sample_weights),
        replacement=True,
    )
    return DataLoader(dataset, batch_size=batch_size, sampler=sampler)


def compute_class_weights(y: np.ndarray, indices: np.ndarray, num_classes: int) -> torch.Tensor:
    y_subset = y[indices]
    class_counts = np.bincount(y_subset, minlength=num_classes)
    weights = class_counts.sum() / (num_classes * np.maximum(class_counts, 1))
    return torch.as_tensor(weights, dtype=torch.float32)


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[dict[str, float], np.ndarray, np.ndarray]:
    model.eval()
    losses: list[float] = []
    y_true: list[int] = []
    y_pred: list[int] = []

    with torch.no_grad():
        for batch_x, batch_y in loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            predictions = torch.argmax(logits, dim=1)

            losses.append(float(loss.item()))
            y_true.extend(batch_y.cpu().numpy().tolist())
            y_pred.extend(predictions.cpu().numpy().tolist())

    y_true_array = np.asarray(y_true, dtype=np.int64)
    y_pred_array = np.asarray(y_pred, dtype=np.int64)
    metrics = {
        "loss": float(np.mean(losses)) if losses else 0.0,
        "accuracy": float(accuracy_score(y_true_array, y_pred_array)),
        "f1_macro": float(f1_score(y_true_array, y_pred_array, average="macro")),
        "f1_weighted": float(f1_score(y_true_array, y_pred_array, average="weighted")),
    }
    return metrics, y_true_array, y_pred_array


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    device = resolve_device(args.device)

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Prepared dataset not found: {data_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle = np.load(data_path, allow_pickle=False)
    x = bundle["x"]
    y = bundle["y"]
    labels = bundle["labels"].tolist()
    if x.ndim != 2:
        raise ValueError(f"Expected x to have shape [N, packet_size], got {x.shape}")

    all_indices = np.arange(len(y))
    train_val_indices, test_indices = train_test_split(
        all_indices,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=y,
    )
    train_indices, val_indices = train_test_split(
        train_val_indices,
        test_size=args.val_size,
        random_state=args.seed,
        stratify=y[train_val_indices],
    )

    train_loader = build_train_loader(x, y, train_indices, args.batch_size)
    val_loader = build_eval_loader(x, y, val_indices, args.batch_size)
    test_loader = build_eval_loader(x, y, test_indices, args.batch_size)

    class_weights = compute_class_weights(y, train_indices, num_classes=len(labels)).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=args.label_smoothing)

    model = CLSTMClassifier(num_classes=len(labels), dropout=args.dropout).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=args.scheduler_patience,
        min_lr=args.min_learning_rate,
    )

    history: list[dict[str, float]] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_epoch = 0
    best_val_macro_f1 = -1.0
    best_val_metrics: dict[str, float] | None = None
    patience_counter = 0

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_losses: list[float] = []

        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            optimizer.zero_grad(set_to_none=True)
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            if args.grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            optimizer.step()
            train_losses.append(float(loss.item()))

        val_metrics, _, _ = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_metrics["f1_macro"])

        history_row = {
            "epoch": epoch,
            "train_loss": float(np.mean(train_losses)) if train_losses else 0.0,
            "val_loss": val_metrics["loss"],
            "val_accuracy": val_metrics["accuracy"],
            "val_f1_macro": val_metrics["f1_macro"],
            "val_f1_weighted": val_metrics["f1_weighted"],
            "learning_rate": float(optimizer.param_groups[0]["lr"]),
        }
        history.append(history_row)

        if val_metrics["f1_macro"] > best_val_macro_f1:
            best_val_macro_f1 = val_metrics["f1_macro"]
            best_epoch = epoch
            best_val_metrics = dict(val_metrics)
            best_state = copy.deepcopy(model.state_dict())
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= args.early_stop_patience:
                break

    if best_state is None:
        raise RuntimeError("Training finished without producing a best checkpoint.")

    model.load_state_dict(best_state)

    test_metrics, y_test, test_predictions = evaluate(model, test_loader, criterion, device)
    report_text = classification_report(
        y_test,
        test_predictions,
        target_names=labels,
        digits=4,
        zero_division=0,
    )
    report_dict = classification_report(
        y_test,
        test_predictions,
        target_names=labels,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    cm = confusion_matrix(y_test, test_predictions, labels=np.arange(len(labels)))

    metrics = {
        "data_path": str(data_path),
        "samples_total": int(len(y)),
        "samples_train": int(len(train_indices)),
        "samples_val": int(len(val_indices)),
        "samples_test": int(len(test_indices)),
        "num_classes": int(len(labels)),
        "packet_size": int(x.shape[1]),
        "batch_size": int(args.batch_size),
        "epochs_requested": int(args.epochs),
        "epochs_trained": int(len(history)),
        "best_epoch": int(best_epoch),
        "learning_rate": float(args.learning_rate),
        "weight_decay": float(args.weight_decay),
        "dropout": float(args.dropout),
        "label_smoothing": float(args.label_smoothing),
        "seed": int(args.seed),
        "device": str(device),
        "test_loss": test_metrics["loss"],
        "accuracy": test_metrics["accuracy"],
        "f1_macro": test_metrics["f1_macro"],
        "f1_weighted": test_metrics["f1_weighted"],
        "best_val_metrics": best_val_metrics,
    }

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    (output_dir / "classification_report.json").write_text(json.dumps(report_dict, indent=2), encoding="utf-8")
    (output_dir / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    save_confusion_matrix(cm, labels, output_dir / "confusion_matrix.png")
    np.savez_compressed(
        output_dir / "splits.npz",
        train_indices=train_indices,
        val_indices=val_indices,
        test_indices=test_indices,
    )
    torch.save(
        {
            "state_dict": model.state_dict(),
            "labels": labels,
            "packet_size": int(x.shape[1]),
            "model_type": "c_lstm",
            "training_recipe": "improved_local",
        },
        output_dir / "model.pt",
    )

    print("Improved training finished.")
    print(f"Best epoch : {best_epoch}")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"F1 (macro) : {metrics['f1_macro']:.4f}")
    print(f"F1 (weight): {metrics['f1_weighted']:.4f}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
