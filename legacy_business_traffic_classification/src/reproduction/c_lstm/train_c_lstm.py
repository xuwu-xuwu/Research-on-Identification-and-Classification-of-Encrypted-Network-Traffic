#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class CLSTMClassifier(nn.Module):
    def __init__(self, num_classes: int, dropout: float = 0.05) -> None:
        super().__init__()
        self.conv1 = nn.Conv1d(1, 50, kernel_size=5, stride=3)
        self.conv2 = nn.Conv1d(50, 50, kernel_size=4, stride=3)
        # The paper's table reports an output length of 81, which is consistent with stride=2.
        self.pool = nn.MaxPool1d(kernel_size=3, stride=2)
        self.lstm = nn.LSTM(input_size=81, hidden_size=50, batch_first=True)
        self.fc1 = nn.Linear(2500, 500)
        self.fc2 = nn.Linear(500, 50)
        self.fc3 = nn.Linear(50, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.float() / 255.0
        x = x.unsqueeze(1)
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        if x.shape[1:] != (50, 81):
            raise RuntimeError(f"Unexpected convolution output shape: {tuple(x.shape[1:])}")
        x, _ = self.lstm(x)
        x = torch.flatten(x, start_dim=1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.dropout(self.relu(self.fc2(x)))
        return self.fc3(x)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a paper-style C-LSTM classifier.")
    parser.add_argument("--data", required=True, help="Path to the prepared .npz packet dataset.")
    parser.add_argument("--output-dir", required=True, help="Directory for model outputs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size.")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="Adam learning rate.")
    parser.add_argument("--weight-decay", type=float, default=0.0, help="Adam weight decay.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Hold-out test ratio.")
    parser.add_argument(
        "--cv-folds",
        type=int,
        default=0,
        help="Stratified folds on the training split. 0 disables cross-validation.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda.")
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def resolve_device(device_arg: str) -> torch.device:
    if device_arg == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device_arg)


def build_loader(x: np.ndarray, y: np.ndarray, indices: np.ndarray, batch_size: int, shuffle: bool) -> DataLoader:
    dataset = TensorDataset(
        torch.from_numpy(x[indices]),
        torch.from_numpy(y[indices]),
    )
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def train_one_model(
    x: np.ndarray,
    y: np.ndarray,
    train_indices: np.ndarray,
    eval_indices: np.ndarray,
    num_classes: int,
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[nn.Module, dict[str, float], np.ndarray]:
    model = CLSTMClassifier(num_classes=num_classes).to(device)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )
    criterion = nn.CrossEntropyLoss()

    train_loader = build_loader(x, y, train_indices, args.batch_size, shuffle=True)
    eval_loader = build_loader(x, y, eval_indices, args.batch_size, shuffle=False)

    for _ in range(args.epochs):
        model.train()
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()

    metrics, predictions = evaluate_model(model, eval_loader, device)
    return model, metrics, predictions


def evaluate_model(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[dict[str, float], np.ndarray]:
    model.eval()
    y_true: list[int] = []
    y_pred: list[int] = []
    with torch.no_grad():
        for batch_x, batch_y in loader:
            logits = model(batch_x.to(device))
            predictions = torch.argmax(logits, dim=1).cpu().numpy()
            y_pred.extend(predictions.tolist())
            y_true.extend(batch_y.numpy().tolist())

    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
    }
    return metrics, np.asarray(y_pred, dtype=np.int64)


def save_confusion_matrix(cm: np.ndarray, labels: list[str], out_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(max(8, len(labels) * 0.9), max(6, len(labels) * 0.7)))
    image = axis.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    axis.set(
        xticks=np.arange(len(labels)),
        yticks=np.arange(len(labels)),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="True label",
        xlabel="Predicted label",
        title="C-LSTM Confusion Matrix",
    )
    plt.setp(axis.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    threshold = cm.max() / 2.0 if cm.size else 0
    for row in range(cm.shape[0]):
        for column in range(cm.shape[1]):
            axis.text(
                column,
                row,
                format(cm[row, column], "d"),
                ha="center",
                va="center",
                color="white" if cm[row, column] > threshold else "black",
                fontsize=8,
            )

    figure.tight_layout()
    figure.savefig(out_path, dpi=160)
    plt.close(figure)


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

    indices = np.arange(len(y))
    train_indices, test_indices = train_test_split(
        indices,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=y,
    )

    cv_summary: dict[str, object] | None = None
    if args.cv_folds and args.cv_folds > 1:
        cv_scores = []
        splitter = StratifiedKFold(n_splits=args.cv_folds, shuffle=True, random_state=args.seed)
        train_targets = y[train_indices]
        for fold_index, (inner_train, inner_val) in enumerate(splitter.split(train_indices, train_targets), start=1):
            fold_train_indices = train_indices[inner_train]
            fold_val_indices = train_indices[inner_val]
            _, fold_metrics, _ = train_one_model(
                x=x,
                y=y,
                train_indices=fold_train_indices,
                eval_indices=fold_val_indices,
                num_classes=len(labels),
                args=args,
                device=device,
            )
            cv_scores.append({"fold": fold_index, **fold_metrics})

        cv_summary = {
            "folds": cv_scores,
            "mean_accuracy": float(np.mean([item["accuracy"] for item in cv_scores])),
            "mean_f1_macro": float(np.mean([item["f1_macro"] for item in cv_scores])),
            "mean_f1_weighted": float(np.mean([item["f1_weighted"] for item in cv_scores])),
        }
        (output_dir / "cv_metrics.json").write_text(json.dumps(cv_summary, indent=2), encoding="utf-8")

    model, test_metrics, test_predictions = train_one_model(
        x=x,
        y=y,
        train_indices=train_indices,
        eval_indices=test_indices,
        num_classes=len(labels),
        args=args,
        device=device,
    )

    y_test = y[test_indices]
    report = classification_report(
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
        "samples_test": int(len(test_indices)),
        "num_classes": int(len(labels)),
        "packet_size": int(x.shape[1]),
        "batch_size": int(args.batch_size),
        "epochs": int(args.epochs),
        "learning_rate": float(args.learning_rate),
        "weight_decay": float(args.weight_decay),
        "seed": int(args.seed),
        "device": str(device),
        **test_metrics,
    }
    if cv_summary is not None:
        metrics["cv_mean_accuracy"] = cv_summary["mean_accuracy"]
        metrics["cv_mean_f1_macro"] = cv_summary["mean_f1_macro"]
        metrics["cv_mean_f1_weighted"] = cv_summary["mean_f1_weighted"]

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "classification_report.txt").write_text(report, encoding="utf-8")
    (output_dir / "classification_report.json").write_text(
        json.dumps(report_dict, indent=2),
        encoding="utf-8",
    )
    save_confusion_matrix(cm, labels, output_dir / "confusion_matrix.png")
    np.savez_compressed(output_dir / "splits.npz", train_indices=train_indices, test_indices=test_indices)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "labels": labels,
            "packet_size": int(x.shape[1]),
        },
        output_dir / "model.pt",
    )

    print("Training finished.")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"F1 (macro) : {metrics['f1_macro']:.4f}")
    print(f"F1 (weight): {metrics['f1_weighted']:.4f}")
    if cv_summary is not None:
        print(f"CV mean acc: {cv_summary['mean_accuracy']:.4f}")
    print(f"Output dir  : {output_dir}")


if __name__ == "__main__":
    main()
