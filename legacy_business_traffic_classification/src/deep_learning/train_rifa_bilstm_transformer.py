#!/usr/bin/env python
"""Train a stronger BiLSTM+Transformer classifier on TrafficFormer-style TSV datasets."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler


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


def load_label_map(path: Path) -> tuple[dict[str, int], list[str]]:
    with path.open("r", encoding="utf-8") as handle:
        label_map = json.load(handle)
    id_to_label = sorted(label_map, key=label_map.get)
    return label_map, id_to_label


def read_tsv_dataset(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rows.append({"label": int(row["label"]), "text_a": row["text_a"].strip()})
    if not rows:
        raise ValueError(f"No rows found in TSV dataset: {path}")
    return rows


def load_vocab(path: Path) -> dict[str, int]:
    token_to_id: dict[str, int] = {}
    with path.open("r", encoding="utf-8") as handle:
        for index, raw in enumerate(handle):
            token = raw.rstrip("\n\r")
            token_to_id[token] = index
    required = {"[PAD]", "[UNK]", "[SEP]"}
    missing = sorted(required - set(token_to_id))
    if missing:
        raise ValueError(f"Vocab is missing required tokens: {missing}")
    return token_to_id


def encode_rows(
    rows: list[dict[str, object]],
    token_to_id: dict[str, int],
    max_seq_length: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    unk_id = token_to_id["[UNK]"]
    pad_id = token_to_id["[PAD]"]

    features = np.full((len(rows), max_seq_length), pad_id, dtype=np.int64)
    lengths = np.zeros(len(rows), dtype=np.int64)
    labels = np.zeros(len(rows), dtype=np.int64)

    for index, row in enumerate(rows):
        tokens = str(row["text_a"]).split()
        token_ids = [token_to_id.get(token, unk_id) for token in tokens[:max_seq_length]]
        seq_len = len(token_ids)
        if seq_len > 0:
            features[index, :seq_len] = np.asarray(token_ids, dtype=np.int64)
        lengths[index] = seq_len
        labels[index] = int(row["label"])

    return features, lengths, labels


def build_loader(
    features: np.ndarray,
    lengths: np.ndarray,
    labels: np.ndarray,
    batch_size: int,
    shuffle: bool,
    sample_weights: np.ndarray | None = None,
) -> DataLoader:
    dataset = TensorDataset(
        torch.from_numpy(features),
        torch.from_numpy(lengths),
        torch.from_numpy(labels),
    )
    sampler = None
    effective_shuffle = shuffle
    if sample_weights is not None:
        sampler = WeightedRandomSampler(
            weights=torch.as_tensor(sample_weights, dtype=torch.double),
            num_samples=len(sample_weights),
            replacement=True,
        )
        effective_shuffle = False
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=effective_shuffle,
        sampler=sampler,
        num_workers=0,
        pin_memory=torch.cuda.is_available(),
    )


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 512) -> None:
        super().__init__()
        position = torch.arange(max_len, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2, dtype=torch.float32) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, d_model, dtype=torch.float32)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0), persistent=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, : x.size(1)]


class AttentionPooling(nn.Module):
    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.score = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        attn_scores = self.score(x).squeeze(-1)
        attn_scores = attn_scores.masked_fill(~mask, -1e9)
        attn_weights = torch.softmax(attn_scores, dim=1)
        return torch.bmm(attn_weights.unsqueeze(1), x).squeeze(1)


class FlowBiLSTMTransformer(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        num_classes: int,
        pad_id: int,
        max_seq_length: int,
        embedding_dim: int = 160,
        lstm_hidden_dim: int = 128,
        lstm_layers: int = 1,
        transformer_layers: int = 2,
        transformer_heads: int = 8,
        transformer_ff_dim: int = 512,
        dropout: float = 0.25,
    ) -> None:
        super().__init__()
        model_dim = lstm_hidden_dim * 2
        self.pad_id = pad_id
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_id)
        self.embedding_dropout = nn.Dropout(dropout)
        self.bilstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=lstm_hidden_dim,
            num_layers=lstm_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )
        self.sequence_proj = nn.Linear(model_dim, model_dim)
        self.position = PositionalEncoding(model_dim, max_len=max_seq_length)
        self.transformer = None
        if transformer_layers > 0:
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=model_dim,
                nhead=transformer_heads,
                dim_feedforward=transformer_ff_dim,
                dropout=dropout,
                activation="gelu",
                batch_first=True,
                norm_first=False,
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=transformer_layers)
        self.attention_pool = AttentionPooling(model_dim)
        self.output_dropout = nn.Dropout(dropout)
        self.classifier = nn.Sequential(
            nn.Linear(model_dim * 3, model_dim),
            nn.LayerNorm(model_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(model_dim, num_classes),
        )

    def forward(self, token_ids: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        mask = token_ids.ne(self.pad_id)
        embedded = self.embedding_dropout(self.embedding(token_ids))

        packed = pack_padded_sequence(
            embedded,
            lengths.clamp(min=1).cpu(),
            batch_first=True,
            enforce_sorted=False,
        )
        packed_out, _ = self.bilstm(packed)
        lstm_out, _ = pad_packed_sequence(
            packed_out,
            batch_first=True,
            total_length=token_ids.size(1),
        )

        sequence = self.sequence_proj(lstm_out)
        sequence = self.position(sequence)
        if self.transformer is not None:
            sequence = self.transformer(sequence, src_key_padding_mask=~mask)

        attn_pooled = self.attention_pool(sequence, mask)
        masked_sequence = sequence.masked_fill(~mask.unsqueeze(-1), -1e9)
        max_pooled = masked_sequence.max(dim=1).values
        max_pooled = torch.where(torch.isfinite(max_pooled), max_pooled, torch.zeros_like(max_pooled))
        mean_pooled = (sequence * mask.unsqueeze(-1)).sum(dim=1) / lengths.clamp(min=1).unsqueeze(1)

        features = torch.cat([attn_pooled, max_pooled, mean_pooled], dim=1)
        features = self.output_dropout(features)
        return self.classifier(features)


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[dict[str, float], np.ndarray, np.ndarray, np.ndarray]:
    model.eval()
    losses: list[float] = []
    y_true: list[int] = []
    y_pred: list[int] = []
    y_prob: list[np.ndarray] = []

    with torch.no_grad():
        for batch_x, batch_len, batch_y in loader:
            batch_x = batch_x.to(device, non_blocking=True)
            batch_len = batch_len.to(device, non_blocking=True)
            batch_y = batch_y.to(device, non_blocking=True)

            logits = model(batch_x, batch_len)
            loss = criterion(logits, batch_y)
            probs = torch.softmax(logits, dim=1)
            preds = torch.argmax(probs, dim=1)

            losses.append(float(loss.item()))
            y_true.extend(batch_y.cpu().numpy().tolist())
            y_pred.extend(preds.cpu().numpy().tolist())
            y_prob.append(probs.cpu().numpy())

    y_true_array = np.asarray(y_true, dtype=np.int64)
    y_pred_array = np.asarray(y_pred, dtype=np.int64)
    y_prob_array = np.concatenate(y_prob, axis=0) if y_prob else np.empty((0, 0), dtype=np.float32)

    metrics = {
        "loss": float(np.mean(losses)) if losses else 0.0,
        "accuracy": float(accuracy_score(y_true_array, y_pred_array)),
        "f1_macro": float(f1_score(y_true_array, y_pred_array, average="macro")),
        "f1_weighted": float(f1_score(y_true_array, y_pred_array, average="weighted")),
    }
    return metrics, y_true_array, y_pred_array, y_prob_array


def save_confusion_matrix(cm: np.ndarray, labels: list[str], out_path: Path) -> None:
    fig_w = max(8, len(labels) * 0.9)
    fig_h = max(6, len(labels) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    image = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    ax.set(
        xticks=np.arange(len(labels)),
        yticks=np.arange(len(labels)),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="True label",
        xlabel="Predicted label",
        title="BiLSTM+Transformer Confusion Matrix",
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    threshold = cm.max() / 2.0 if cm.size else 0
    for row in range(cm.shape[0]):
        for col in range(cm.shape[1]):
            ax.text(
                col,
                row,
                format(cm[row, col], "d"),
                ha="center",
                va="center",
                color="white" if cm[row, col] > threshold else "black",
                fontsize=8,
            )

    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a BiLSTM+Transformer on TrafficFormer-style TSV data.")
    parser.add_argument("--train-path", required=True, help="Training TSV path.")
    parser.add_argument("--dev-path", required=True, help="Validation TSV path.")
    parser.add_argument("--test-path", required=True, help="Test TSV path.")
    parser.add_argument("--label-map-path", required=True, help="Label map JSON path.")
    parser.add_argument("--vocab-path", required=True, help="Vocabulary file path.")
    parser.add_argument("--output-dir", required=True, help="Directory for outputs.")
    parser.add_argument("--run-name", default="run", help="User-facing run label.")
    parser.add_argument("--max-seq-length", type=int, default=320, help="Maximum sequence length.")
    parser.add_argument("--embedding-dim", type=int, default=160, help="Embedding size.")
    parser.add_argument("--lstm-hidden-dim", type=int, default=128, help="BiLSTM hidden size per direction.")
    parser.add_argument("--lstm-layers", type=int, default=1, help="BiLSTM stacked layers.")
    parser.add_argument("--transformer-layers", type=int, default=2, help="Transformer encoder layers.")
    parser.add_argument("--transformer-heads", type=int, default=8, help="Attention heads.")
    parser.add_argument("--transformer-ff-dim", type=int, default=512, help="Transformer feed-forward size.")
    parser.add_argument("--dropout", type=float, default=0.25, help="Dropout rate.")
    parser.add_argument("--batch-size", type=int, default=32, help="Mini-batch size.")
    parser.add_argument("--epochs", type=int, default=40, help="Maximum number of epochs.")
    parser.add_argument("--learning-rate", type=float, default=8e-4, help="AdamW learning rate.")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="AdamW weight decay.")
    parser.add_argument("--label-smoothing", type=float, default=0.02, help="CrossEntropy label smoothing.")
    parser.add_argument("--grad-clip", type=float, default=3.0, help="Gradient clipping threshold.")
    parser.add_argument("--scheduler-patience", type=int, default=3, help="ReduceLROnPlateau patience.")
    parser.add_argument("--early-stop-patience", type=int, default=8, help="Early stopping patience.")
    parser.add_argument("--min-learning-rate", type=float, default=1e-5, help="Scheduler lower bound.")
    parser.add_argument("--use-weighted-sampler", action="store_true", help="Use weighted sampling for the training loader.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    device = resolve_device(args.device)
    if hasattr(torch, "set_float32_matmul_precision"):
        torch.set_float32_matmul_precision("high")

    train_path = Path(args.train_path)
    dev_path = Path(args.dev_path)
    test_path = Path(args.test_path)
    label_map_path = Path(args.label_map_path)
    vocab_path = Path(args.vocab_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in (train_path, dev_path, test_path, label_map_path, vocab_path):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

    _, id_to_label = load_label_map(label_map_path)
    token_to_id = load_vocab(vocab_path)
    train_rows = read_tsv_dataset(train_path)
    dev_rows = read_tsv_dataset(dev_path)
    test_rows = read_tsv_dataset(test_path)

    x_train, len_train, y_train = encode_rows(train_rows, token_to_id, args.max_seq_length)
    x_dev, len_dev, y_dev = encode_rows(dev_rows, token_to_id, args.max_seq_length)
    x_test, len_test, y_test = encode_rows(test_rows, token_to_id, args.max_seq_length)

    class_counts = np.bincount(y_train, minlength=len(id_to_label))
    class_weights = class_counts.sum() / (len(id_to_label) * np.maximum(class_counts, 1))
    class_weights_tensor = torch.as_tensor(class_weights, dtype=torch.float32, device=device)
    train_sample_weights = class_weights[y_train] if args.use_weighted_sampler else None

    train_loader = build_loader(
        x_train,
        len_train,
        y_train,
        args.batch_size,
        shuffle=True,
        sample_weights=train_sample_weights,
    )
    dev_loader = build_loader(x_dev, len_dev, y_dev, args.batch_size, shuffle=False)
    test_loader = build_loader(x_test, len_test, y_test, args.batch_size, shuffle=False)

    model = FlowBiLSTMTransformer(
        vocab_size=len(token_to_id),
        num_classes=len(id_to_label),
        pad_id=token_to_id["[PAD]"],
        max_seq_length=args.max_seq_length,
        embedding_dim=args.embedding_dim,
        lstm_hidden_dim=args.lstm_hidden_dim,
        lstm_layers=args.lstm_layers,
        transformer_layers=args.transformer_layers,
        transformer_heads=args.transformer_heads,
        transformer_ff_dim=args.transformer_ff_dim,
        dropout=args.dropout,
    ).to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=args.scheduler_patience,
        min_lr=args.min_learning_rate,
    )
    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor, label_smoothing=args.label_smoothing)

    history: list[dict[str, float]] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_epoch = 0
    best_val_metrics: dict[str, float] | None = None
    best_val_macro_f1 = -1.0
    patience_counter = 0

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_losses: list[float] = []

        for batch_x, batch_len, batch_y in train_loader:
            batch_x = batch_x.to(device, non_blocking=True)
            batch_len = batch_len.to(device, non_blocking=True)
            batch_y = batch_y.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)
            logits = model(batch_x, batch_len)
            loss = criterion(logits, batch_y)
            loss.backward()
            if args.grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            optimizer.step()
            train_losses.append(float(loss.item()))

        val_metrics, _, _, _ = evaluate(model, dev_loader, criterion, device)
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

    if best_state is None or best_val_metrics is None:
        raise RuntimeError("Training finished without producing a best checkpoint.")

    model.load_state_dict(best_state)
    test_metrics, y_test_eval, test_pred, test_prob = evaluate(model, test_loader, criterion, device)

    report_text = classification_report(
        y_test_eval,
        test_pred,
        target_names=id_to_label,
        digits=4,
        zero_division=0,
    )
    report_dict = classification_report(
        y_test_eval,
        test_pred,
        target_names=id_to_label,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    recalls = recall_score(y_test_eval, test_pred, average=None, zero_division=0)
    cm = confusion_matrix(y_test_eval, test_pred, labels=np.arange(len(id_to_label)))

    confidence = test_prob.max(axis=1)
    sorted_prob = np.sort(test_prob, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2] if test_prob.shape[1] > 1 else np.ones_like(confidence)
    predictions_df = pd.DataFrame(
        {
            "y_true": [id_to_label[idx] for idx in y_test_eval],
            "y_pred": [id_to_label[idx] for idx in test_pred],
            "confidence": confidence,
            "margin_top1_top2": margin,
            "is_correct": y_test_eval == test_pred,
        }
    )

    metrics = {
        "run_name": args.run_name,
        "train_path": str(train_path),
        "dev_path": str(dev_path),
        "test_path": str(test_path),
        "label_map_path": str(label_map_path),
        "vocab_path": str(vocab_path),
        "samples_train": int(len(train_rows)),
        "samples_dev": int(len(dev_rows)),
        "samples_test": int(len(test_rows)),
        "max_seq_length": int(args.max_seq_length),
        "vocab_size": int(len(token_to_id)),
        "num_classes": int(len(id_to_label)),
        "class_names": id_to_label,
        "embedding_dim": int(args.embedding_dim),
        "lstm_hidden_dim": int(args.lstm_hidden_dim),
        "lstm_layers": int(args.lstm_layers),
        "transformer_layers": int(args.transformer_layers),
        "transformer_heads": int(args.transformer_heads),
        "transformer_ff_dim": int(args.transformer_ff_dim),
        "batch_size": int(args.batch_size),
        "epochs_requested": int(args.epochs),
        "epochs_trained": int(len(history)),
        "best_epoch": int(best_epoch),
        "learning_rate": float(args.learning_rate),
        "weight_decay": float(args.weight_decay),
        "dropout": float(args.dropout),
        "label_smoothing": float(args.label_smoothing),
        "use_weighted_sampler": bool(args.use_weighted_sampler),
        "seed": int(args.seed),
        "device": str(device),
        "average_sequence_length": float(np.mean(len_train)),
        "accuracy": float(test_metrics["accuracy"]),
        "f1_macro": float(test_metrics["f1_macro"]),
        "f1_weighted": float(test_metrics["f1_weighted"]),
        "test_loss": float(test_metrics["loss"]),
        "class_recalls": {name: float(value) for name, value in zip(id_to_label, recalls)},
        "best_val_metrics": best_val_metrics,
    }

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    pd.DataFrame(report_dict).transpose().to_csv(output_dir / "classification_report.csv", index=True)
    pd.DataFrame(cm, index=id_to_label, columns=id_to_label).to_csv(output_dir / "confusion_matrix.csv")
    predictions_df.to_csv(output_dir / "test_predictions.csv", index=False)
    np.savez_compressed(output_dir / "encoded_test_outputs.npz", y_true=y_test_eval, y_pred=test_pred, y_prob=test_prob)
    save_confusion_matrix(cm, id_to_label, output_dir / "confusion_matrix.png")

    torch.save(
        {
            "state_dict": model.state_dict(),
            "model_type": "rifa_bilstm_transformer",
            "num_classes": len(id_to_label),
            "class_names": id_to_label,
            "vocab_size": len(token_to_id),
            "pad_id": token_to_id["[PAD]"],
            "max_seq_length": args.max_seq_length,
            "embedding_dim": args.embedding_dim,
            "lstm_hidden_dim": args.lstm_hidden_dim,
            "lstm_layers": args.lstm_layers,
            "transformer_layers": args.transformer_layers,
            "transformer_heads": args.transformer_heads,
            "transformer_ff_dim": args.transformer_ff_dim,
            "dropout": args.dropout,
            "metrics": metrics,
        },
        output_dir / "model.pt",
    )

    print("BiLSTM+Transformer training finished.")
    print(f"Run name   : {args.run_name}")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"F1 (macro) : {metrics['f1_macro']:.4f}")
    print(f"F1 (weight): {metrics['f1_weighted']:.4f}")
    print(f"Best epoch : {metrics['best_epoch']}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
