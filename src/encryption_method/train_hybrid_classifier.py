#!/usr/bin/env python
"""Train a new hybrid deep model for encryption-method identification.

Stage 1:
- binary pretraining on ENCRYPTED vs NON_ENCRYPTED

Stage 2:
- multiclass fine-tuning on unified encryption-method labels

The model is built from scratch for the encryption-method pivot. It uses:
- aligned numeric flow features
- dataset-source embedding
- transport embedding
- optional token sequence branch for PCAP-derived flow samples
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler


COMMON_NUMERIC_FEATURES = [
    "duration",
    "packet_count",
    "fwd_packet_count",
    "bwd_packet_count",
    "byte_count",
    "fwd_byte_count",
    "bwd_byte_count",
    "packets_per_second",
    "bytes_per_second",
    "mean_packet_len",
    "std_packet_len",
    "min_packet_len",
    "max_packet_len",
    "mean_iat",
    "std_iat",
    "min_iat",
    "max_iat",
    "direction_packet_ratio",
    "direction_byte_ratio",
    "avg_packet_size",
    "encrypted_packet_ratio",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train hybrid encryption-method classifier.")
    parser.add_argument(
        "--data-dir",
        default="data/unified_encryption_method_v1",
        help="Directory containing unified csv files.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/encryption_method/hybrid_unified_v1",
        help="Directory for logs, metrics, and model outputs.",
    )
    parser.add_argument("--binary-epochs", type=int, default=8, help="Binary pretraining epochs.")
    parser.add_argument("--multiclass-epochs", type=int, default=18, help="Multiclass fine-tuning epochs.")
    parser.add_argument("--batch-size", type=int, default=512, help="Batch size.")
    parser.add_argument("--binary-learning-rate", type=float, default=1e-3, help="Binary pretraining LR.")
    parser.add_argument("--multiclass-learning-rate", type=float, default=7e-4, help="Multiclass LR.")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="AdamW weight decay.")
    parser.add_argument(
        "--binary-sampler-power",
        type=float,
        default=1.0,
        help="Exponent for inverse-frequency sampling during binary pretraining.",
    )
    parser.add_argument(
        "--multiclass-sampler-power",
        type=float,
        default=0.5,
        help="Exponent for inverse-frequency sampling during multiclass fine-tuning.",
    )
    parser.add_argument(
        "--binary-class-weight-power",
        type=float,
        default=1.0,
        help="Exponent for inverse-frequency loss weights during binary pretraining.",
    )
    parser.add_argument(
        "--multiclass-class-weight-power",
        type=float,
        default=0.5,
        help="Exponent for inverse-frequency loss weights during multiclass fine-tuning.",
    )
    parser.add_argument("--dropout", type=float, default=0.25, help="Dropout rate.")
    parser.add_argument("--hidden-dim", type=int, default=192, help="Main hidden dimension.")
    parser.add_argument("--seq-embedding-dim", type=int, default=64, help="Sequence token embedding size.")
    parser.add_argument("--source-embedding-dim", type=int, default=8, help="Source embedding size.")
    parser.add_argument("--transport-embedding-dim", type=int, default=8, help="Transport embedding size.")
    parser.add_argument("--max-seq-len", type=int, default=160, help="Maximum sequence length.")
    parser.add_argument("--min-token-freq", type=int, default=2, help="Min token frequency for vocab.")
    parser.add_argument("--label-smoothing", type=float, default=0.02, help="CrossEntropy label smoothing.")
    parser.add_argument("--grad-clip", type=float, default=5.0, help="Gradient clipping.")
    parser.add_argument("--scheduler-patience", type=int, default=2, help="ReduceLROnPlateau patience.")
    parser.add_argument("--early-stop-patience", type=int, default=5, help="Early stopping patience.")
    parser.add_argument("--min-learning-rate", type=float, default=1e-5, help="Scheduler lower bound.")
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


def safe_log1p(values: np.ndarray) -> np.ndarray:
    return np.sign(values) * np.log1p(np.abs(values))


class NumericPreprocessor:
    def __init__(self, medians: np.ndarray, means: np.ndarray, stds: np.ndarray) -> None:
        self.medians = medians.astype(np.float32)
        self.means = means.astype(np.float32)
        self.stds = stds.astype(np.float32)

    @classmethod
    def fit(cls, frame: pd.DataFrame, feature_cols: list[str]) -> "NumericPreprocessor":
        values = frame[feature_cols].to_numpy(dtype=np.float32, copy=True)
        medians = np.nanmedian(values, axis=0)
        medians = np.where(np.isnan(medians), 0.0, medians)
        missing_mask = np.isnan(values)
        filled = np.where(missing_mask, medians, values)
        logged = safe_log1p(filled)
        means = logged.mean(axis=0)
        stds = logged.std(axis=0)
        stds = np.where(stds < 1e-6, 1.0, stds)
        return cls(medians=medians, means=means, stds=stds)

    def transform(self, frame: pd.DataFrame, feature_cols: list[str]) -> tuple[np.ndarray, np.ndarray]:
        values = frame[feature_cols].to_numpy(dtype=np.float32, copy=True)
        missing_mask = np.isnan(values).astype(np.float32)
        filled = np.where(np.isnan(values), self.medians, values)
        logged = safe_log1p(filled)
        normalized = (logged - self.means) / self.stds
        return normalized.astype(np.float32), missing_mask.astype(np.float32)

    def to_dict(self, feature_cols: list[str]) -> dict[str, list[float] | list[str]]:
        return {
            "feature_cols": feature_cols,
            "medians": self.medians.tolist(),
            "means": self.means.tolist(),
            "stds": self.stds.tolist(),
        }


def build_vocab(sequences: list[str], min_token_freq: int) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for text in sequences:
        if not text:
            continue
        counter.update(token for token in text.split() if token)

    vocab = {"[PAD]": 0, "[UNK]": 1}
    for token, count in counter.most_common():
        if count < min_token_freq:
            break
        vocab[token] = len(vocab)
    return vocab


def encode_sequence(text: str, vocab: dict[str, int], max_seq_len: int) -> list[int]:
    if not text:
        return []
    unk_id = vocab["[UNK]"]
    tokens = [vocab.get(token, unk_id) for token in text.split()[:max_seq_len] if token]
    return tokens


class HybridDataset(Dataset):
    def __init__(
        self,
        frame: pd.DataFrame,
        feature_cols: list[str],
        preprocessor: NumericPreprocessor,
        vocab: dict[str, int],
        source_map: dict[str, int],
        transport_map: dict[str, int],
        label_map: dict[str, int] | None,
        max_seq_len: int,
    ) -> None:
        self.frame = frame.reset_index(drop=True).copy()
        self.feature_cols = feature_cols
        self.numeric_values, self.missing_masks = preprocessor.transform(self.frame, feature_cols)
        self.source_ids = self.frame["source_name"].map(source_map).to_numpy(dtype=np.int64)
        self.transport_ids = self.frame["transport"].map(transport_map).to_numpy(dtype=np.int64)
        if label_map is None:
            self.label_ids = np.full(len(self.frame), -1, dtype=np.int64)
        else:
            self.label_ids = self.frame["label"].map(label_map).to_numpy(dtype=np.int64)
        self.sequence_ids = [
            encode_sequence(text, vocab=vocab, max_seq_len=max_seq_len)
            for text in self.frame["sequence_text"].astype(str).tolist()
        ]

    def __len__(self) -> int:
        return len(self.frame)

    def __getitem__(self, index: int) -> dict[str, object]:
        return {
            "numeric": self.numeric_values[index],
            "missing_mask": self.missing_masks[index],
            "source_id": int(self.source_ids[index]),
            "transport_id": int(self.transport_ids[index]),
            "sequence_ids": self.sequence_ids[index],
            "label_id": int(self.label_ids[index]),
            "source_name": self.frame.at[index, "source_name"],
        }


def collate_batch(batch: list[dict[str, object]]) -> dict[str, object]:
    numeric = torch.as_tensor(np.stack([item["numeric"] for item in batch]), dtype=torch.float32)
    missing_mask = torch.as_tensor(np.stack([item["missing_mask"] for item in batch]), dtype=torch.float32)
    source_ids = torch.as_tensor([item["source_id"] for item in batch], dtype=torch.long)
    transport_ids = torch.as_tensor([item["transport_id"] for item in batch], dtype=torch.long)
    label_ids = torch.as_tensor([item["label_id"] for item in batch], dtype=torch.long)
    source_names = [str(item["source_name"]) for item in batch]

    sequences = []
    lengths = []
    for item in batch:
        seq = torch.as_tensor(item["sequence_ids"], dtype=torch.long)
        sequences.append(seq)
        lengths.append(int(seq.numel()))
    if sequences:
        padded = pad_sequence(sequences, batch_first=True, padding_value=0)
    else:
        padded = torch.zeros((len(batch), 0), dtype=torch.long)
    lengths_tensor = torch.as_tensor(lengths, dtype=torch.long)

    return {
        "numeric": numeric,
        "missing_mask": missing_mask,
        "source_ids": source_ids,
        "transport_ids": transport_ids,
        "sequence_ids": padded,
        "sequence_lengths": lengths_tensor,
        "label_ids": label_ids,
        "source_names": source_names,
    }


class HybridClassifier(nn.Module):
    def __init__(
        self,
        num_numeric: int,
        vocab_size: int,
        num_sources: int,
        num_transports: int,
        num_classes: int,
        hidden_dim: int,
        seq_embedding_dim: int,
        source_embedding_dim: int,
        transport_embedding_dim: int,
        dropout: float,
    ) -> None:
        super().__init__()
        numeric_dim = num_numeric * 2
        self.numeric_encoder = nn.Sequential(
            nn.LayerNorm(numeric_dim),
            nn.Linear(numeric_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
        )
        self.source_embedding = nn.Embedding(num_sources, source_embedding_dim)
        self.transport_embedding = nn.Embedding(num_transports, transport_embedding_dim)

        self.seq_embedding = nn.Embedding(vocab_size, seq_embedding_dim, padding_idx=0)
        self.seq_convs = nn.ModuleList(
            [
                nn.Conv1d(seq_embedding_dim, hidden_dim // 3, kernel_size=3, padding=1),
                nn.Conv1d(seq_embedding_dim, hidden_dim // 3, kernel_size=5, padding=2),
                nn.Conv1d(seq_embedding_dim, hidden_dim // 3, kernel_size=7, padding=3),
            ]
        )
        self.seq_dropout = nn.Dropout(dropout)

        fused_dim = hidden_dim + source_embedding_dim + transport_embedding_dim + (hidden_dim // 3) * 3
        self.fusion = nn.Sequential(
            nn.LayerNorm(fused_dim),
            nn.Linear(fused_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
        )
        self.classifier = nn.Linear(hidden_dim, num_classes)

    def encode_sequence(self, sequence_ids: torch.Tensor, sequence_lengths: torch.Tensor) -> torch.Tensor:
        if sequence_ids.size(1) == 0:
            return torch.zeros((sequence_ids.size(0), sum(conv.out_channels for conv in self.seq_convs)), device=sequence_ids.device)

        embedded = self.seq_embedding(sequence_ids).transpose(1, 2)
        conv_features = []
        for conv in self.seq_convs:
            activations = torch.relu(conv(embedded))
            pooled = torch.max(activations, dim=2).values
            conv_features.append(pooled)
        features = torch.cat(conv_features, dim=1)
        has_sequence = (sequence_lengths > 0).float().unsqueeze(1)
        return self.seq_dropout(features * has_sequence)

    def forward(
        self,
        numeric: torch.Tensor,
        missing_mask: torch.Tensor,
        source_ids: torch.Tensor,
        transport_ids: torch.Tensor,
        sequence_ids: torch.Tensor,
        sequence_lengths: torch.Tensor,
    ) -> torch.Tensor:
        numeric_input = torch.cat([numeric, missing_mask], dim=1)
        numeric_features = self.numeric_encoder(numeric_input)
        source_features = self.source_embedding(source_ids)
        transport_features = self.transport_embedding(transport_ids)
        sequence_features = self.encode_sequence(sequence_ids, sequence_lengths)
        fused = torch.cat([numeric_features, source_features, transport_features, sequence_features], dim=1)
        fused = self.fusion(fused)
        return self.classifier(fused)


def compute_sample_weights(labels: np.ndarray, power: float = 1.0) -> np.ndarray:
    counts = np.bincount(labels)
    counts = np.maximum(counts, 1)
    base_weights = counts.sum() / (len(counts) * counts)
    class_weights = np.power(base_weights.astype(np.float64), power)
    return class_weights[labels]


def build_loader(
    dataset: HybridDataset,
    batch_size: int,
    weighted: bool,
    shuffle: bool,
    sampler_power: float = 1.0,
) -> DataLoader:
    if weighted:
        labels = dataset.label_ids
        sample_weights = compute_sample_weights(labels, power=sampler_power)
        sampler = WeightedRandomSampler(
            weights=torch.as_tensor(sample_weights, dtype=torch.double),
            num_samples=len(sample_weights),
            replacement=True,
        )
        return DataLoader(
            dataset,
            batch_size=batch_size,
            sampler=sampler,
            collate_fn=collate_batch,
            num_workers=0,
            pin_memory=torch.cuda.is_available(),
        )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        collate_fn=collate_batch,
        num_workers=0,
        pin_memory=torch.cuda.is_available(),
    )


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[dict[str, float], np.ndarray, np.ndarray, list[str]]:
    model.eval()
    losses: list[float] = []
    y_true: list[int] = []
    y_pred: list[int] = []
    source_names_all: list[str] = []

    with torch.no_grad():
        for batch in loader:
            numeric = batch["numeric"].to(device, non_blocking=True)
            missing_mask = batch["missing_mask"].to(device, non_blocking=True)
            source_ids = batch["source_ids"].to(device, non_blocking=True)
            transport_ids = batch["transport_ids"].to(device, non_blocking=True)
            sequence_ids = batch["sequence_ids"].to(device, non_blocking=True)
            sequence_lengths = batch["sequence_lengths"].to(device, non_blocking=True)
            label_ids = batch["label_ids"].to(device, non_blocking=True)

            logits = model(
                numeric=numeric,
                missing_mask=missing_mask,
                source_ids=source_ids,
                transport_ids=transport_ids,
                sequence_ids=sequence_ids,
                sequence_lengths=sequence_lengths,
            )
            loss = criterion(logits, label_ids)
            predictions = torch.argmax(logits, dim=1)

            losses.append(float(loss.item()))
            y_true.extend(label_ids.cpu().numpy().tolist())
            y_pred.extend(predictions.cpu().numpy().tolist())
            source_names_all.extend(batch["source_names"])

    y_true_array = np.asarray(y_true, dtype=np.int64)
    y_pred_array = np.asarray(y_pred, dtype=np.int64)
    metrics = {
        "loss": float(np.mean(losses)) if losses else 0.0,
        "accuracy": float(accuracy_score(y_true_array, y_pred_array)),
        "f1_macro": float(f1_score(y_true_array, y_pred_array, average="macro")),
        "f1_weighted": float(f1_score(y_true_array, y_pred_array, average="weighted")),
    }
    return metrics, y_true_array, y_pred_array, source_names_all


def predict_classes(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
) -> np.ndarray:
    model.eval()
    predictions: list[int] = []
    with torch.no_grad():
        for batch in loader:
            numeric = batch["numeric"].to(device, non_blocking=True)
            missing_mask = batch["missing_mask"].to(device, non_blocking=True)
            source_ids = batch["source_ids"].to(device, non_blocking=True)
            transport_ids = batch["transport_ids"].to(device, non_blocking=True)
            sequence_ids = batch["sequence_ids"].to(device, non_blocking=True)
            sequence_lengths = batch["sequence_lengths"].to(device, non_blocking=True)
            logits = model(
                numeric=numeric,
                missing_mask=missing_mask,
                source_ids=source_ids,
                transport_ids=transport_ids,
                sequence_ids=sequence_ids,
                sequence_lengths=sequence_lengths,
            )
            predictions.extend(torch.argmax(logits, dim=1).cpu().numpy().tolist())
    return np.asarray(predictions, dtype=np.int64)


def train_stage(
    model: nn.Module,
    train_loader: DataLoader,
    valid_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.ReduceLROnPlateau,
    criterion: nn.Module,
    device: torch.device,
    epochs: int,
    grad_clip: float,
    early_stop_patience: int,
) -> tuple[list[dict[str, float]], dict[str, torch.Tensor], int, dict[str, float]]:
    history: list[dict[str, float]] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_epoch = 0
    best_val_metrics: dict[str, float] | None = None
    best_macro_f1 = -1.0
    patience_counter = 0

    for epoch in range(1, epochs + 1):
        model.train()
        train_losses: list[float] = []
        for batch in train_loader:
            numeric = batch["numeric"].to(device, non_blocking=True)
            missing_mask = batch["missing_mask"].to(device, non_blocking=True)
            source_ids = batch["source_ids"].to(device, non_blocking=True)
            transport_ids = batch["transport_ids"].to(device, non_blocking=True)
            sequence_ids = batch["sequence_ids"].to(device, non_blocking=True)
            sequence_lengths = batch["sequence_lengths"].to(device, non_blocking=True)
            label_ids = batch["label_ids"].to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)
            logits = model(
                numeric=numeric,
                missing_mask=missing_mask,
                source_ids=source_ids,
                transport_ids=transport_ids,
                sequence_ids=sequence_ids,
                sequence_lengths=sequence_lengths,
            )
            loss = criterion(logits, label_ids)
            loss.backward()
            if grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            optimizer.step()
            train_losses.append(float(loss.item()))

        val_metrics, _, _, _ = evaluate(model, valid_loader, criterion, device)
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

        if val_metrics["f1_macro"] > best_macro_f1:
            best_macro_f1 = val_metrics["f1_macro"]
            best_epoch = epoch
            best_val_metrics = dict(val_metrics)
            best_state = copy.deepcopy(model.state_dict())
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= early_stop_patience:
                break

    if best_state is None or best_val_metrics is None:
        raise RuntimeError("Training ended without a best checkpoint.")

    return history, best_state, best_epoch, best_val_metrics


def transfer_encoder_weights(source_model: HybridClassifier, target_model: HybridClassifier) -> None:
    source_state = source_model.state_dict()
    target_state = target_model.state_dict()
    copied = {
        key: value
        for key, value in source_state.items()
        if key in target_state and value.shape == target_state[key].shape and not key.startswith("classifier.")
    }
    target_state.update(copied)
    target_model.load_state_dict(target_state)


def compute_class_weight_tensor(
    label_ids: np.ndarray,
    device: torch.device,
    power: float = 1.0,
) -> torch.Tensor:
    counts = np.bincount(label_ids)
    counts = np.maximum(counts, 1)
    base_weights = counts.sum() / (len(counts) * counts)
    weights = np.power(base_weights.astype(np.float32), power)
    return torch.as_tensor(weights, dtype=torch.float32, device=device)


def make_label_map(labels: list[str]) -> dict[str, int]:
    return {label: index for index, label in enumerate(labels)}


def save_report_artifacts(
    output_dir: Path,
    label_names: list[str],
    y_true: np.ndarray,
    y_pred: np.ndarray,
    source_names: list[str],
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    label_ids = np.arange(len(label_names))
    report_text = classification_report(
        y_true,
        y_pred,
        labels=label_ids,
        target_names=label_names,
        digits=4,
        zero_division=0,
    )
    report_dict = classification_report(
        y_true,
        y_pred,
        labels=label_ids,
        target_names=label_names,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    confusion = confusion_matrix(y_true, y_pred, labels=label_ids)
    recalls = recall_score(y_true, y_pred, average=None, labels=label_ids)

    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    pd.DataFrame(report_dict).transpose().to_csv(output_dir / "classification_report.csv", index=True)
    pd.DataFrame(confusion, index=label_names, columns=label_names).to_csv(output_dir / "confusion_matrix.csv")

    prediction_frame = pd.DataFrame(
        {
            "source_name": source_names,
            "y_true_id": y_true,
            "y_true": [label_names[index] for index in y_true],
            "y_pred_id": y_pred,
            "y_pred": [label_names[index] for index in y_pred],
        }
    )
    prediction_frame.to_csv(output_dir / "test_predictions.csv", index=False)

    per_source_rows = []
    for source_name, group in prediction_frame.groupby("source_name"):
        true_ids = group["y_true_id"].to_numpy(dtype=np.int64)
        pred_ids = group["y_pred_id"].to_numpy(dtype=np.int64)
        per_source_rows.append(
            {
                "source_name": source_name,
                "samples": int(len(group)),
                "accuracy": float(accuracy_score(true_ids, pred_ids)),
                "f1_macro": float(f1_score(true_ids, pred_ids, average="macro")),
                "f1_weighted": float(f1_score(true_ids, pred_ids, average="weighted")),
            }
        )
    pd.DataFrame(per_source_rows).sort_values("source_name").to_csv(output_dir / "per_source_metrics.csv", index=False)

    return {
        "classification_report": report_dict,
        "class_recalls": {name: float(recall) for name, recall in zip(label_names, recalls)},
        "report_text": report_text,
    }


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    device = resolve_device(args.device)
    if hasattr(torch, "set_float32_matmul_precision"):
        torch.set_float32_matmul_precision("high")

    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    binary_path = data_dir / "binary_pretrain.csv"
    multiclass_path = data_dir / "multiclass_finetune.csv"
    metadata_path = data_dir / "metadata.json"

    for path in (binary_path, multiclass_path, metadata_path):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    feature_cols = list(metadata["common_numeric_features"])

    binary_frame = pd.read_csv(binary_path, low_memory=False)
    multiclass_frame = pd.read_csv(multiclass_path, low_memory=False)

    binary_frame["label"] = binary_frame["binary_label"].astype(str)
    multiclass_frame["label"] = multiclass_frame["final_label"].astype(str)

    binary_train = binary_frame.loc[binary_frame["split"] == "train"].copy()
    binary_valid = binary_frame.loc[binary_frame["split"] == "valid"].copy()
    binary_test = binary_frame.loc[binary_frame["split"] == "test"].copy()

    multiclass_test_full = multiclass_frame.loc[multiclass_frame["split"] == "test"].copy()
    encrypted_label_names = [label for label in metadata["final_label_order"] if label != "NON_ENCRYPTED"]
    encrypted_label_map = make_label_map(encrypted_label_names)

    multiclass_train = multiclass_frame.loc[
        (multiclass_frame["split"] == "train") & (multiclass_frame["final_label"] != "NON_ENCRYPTED")
    ].copy()
    multiclass_valid = multiclass_frame.loc[
        (multiclass_frame["split"] == "valid") & (multiclass_frame["final_label"] != "NON_ENCRYPTED")
    ].copy()
    multiclass_test = multiclass_frame.loc[
        (multiclass_frame["split"] == "test") & (multiclass_frame["final_label"] != "NON_ENCRYPTED")
    ].copy()

    preprocessor = NumericPreprocessor.fit(binary_train, feature_cols=feature_cols)

    vocab_sequences = pd.concat(
        [
            binary_train["sequence_text"].astype(str),
            multiclass_train["sequence_text"].astype(str),
        ],
        ignore_index=True,
    ).tolist()
    vocab = build_vocab(vocab_sequences, min_token_freq=args.min_token_freq)

    source_values = sorted(
        set(binary_frame["source_name"].astype(str).tolist()) | set(multiclass_frame["source_name"].astype(str).tolist())
    )
    transport_values = sorted(
        set(binary_frame["transport"].astype(str).tolist()) | set(multiclass_frame["transport"].astype(str).tolist())
    )
    source_map = {value: index for index, value in enumerate(source_values)}
    transport_map = {value: index for index, value in enumerate(transport_values)}

    binary_label_names = list(metadata["binary_label_order"])
    multiclass_label_names = encrypted_label_names
    binary_label_map = make_label_map(binary_label_names)
    multiclass_label_map = encrypted_label_map

    binary_train_ds = HybridDataset(
        frame=binary_train,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=binary_label_map,
        max_seq_len=args.max_seq_len,
    )
    binary_valid_ds = HybridDataset(
        frame=binary_valid,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=binary_label_map,
        max_seq_len=args.max_seq_len,
    )
    binary_test_ds = HybridDataset(
        frame=binary_test,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=binary_label_map,
        max_seq_len=args.max_seq_len,
    )

    multiclass_train_ds = HybridDataset(
        frame=multiclass_train,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=multiclass_label_map,
        max_seq_len=args.max_seq_len,
    )
    multiclass_valid_ds = HybridDataset(
        frame=multiclass_valid,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=multiclass_label_map,
        max_seq_len=args.max_seq_len,
    )
    multiclass_test_ds = HybridDataset(
        frame=multiclass_test,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=multiclass_label_map,
        max_seq_len=args.max_seq_len,
    )
    multiclass_test_full_binary = multiclass_test_full.copy()
    multiclass_test_full_binary["label"] = multiclass_test_full_binary["binary_label"].astype(str)
    multiclass_test_full_binary_ds = HybridDataset(
        frame=multiclass_test_full_binary,
        feature_cols=feature_cols,
        preprocessor=preprocessor,
        vocab=vocab,
        source_map=source_map,
        transport_map=transport_map,
        label_map=binary_label_map,
        max_seq_len=args.max_seq_len,
    )

    binary_train_loader = build_loader(
        binary_train_ds,
        batch_size=args.batch_size,
        weighted=True,
        shuffle=False,
        sampler_power=args.binary_sampler_power,
    )
    binary_valid_loader = build_loader(binary_valid_ds, batch_size=args.batch_size, weighted=False, shuffle=False)
    binary_test_loader = build_loader(binary_test_ds, batch_size=args.batch_size, weighted=False, shuffle=False)

    multiclass_train_loader = build_loader(
        multiclass_train_ds,
        batch_size=args.batch_size,
        weighted=True,
        shuffle=False,
        sampler_power=args.multiclass_sampler_power,
    )
    multiclass_valid_loader = build_loader(multiclass_valid_ds, batch_size=args.batch_size, weighted=False, shuffle=False)
    multiclass_test_loader = build_loader(multiclass_test_ds, batch_size=args.batch_size, weighted=False, shuffle=False)
    multiclass_test_full_binary_loader = build_loader(
        multiclass_test_full_binary_ds,
        batch_size=args.batch_size,
        weighted=False,
        shuffle=False,
    )

    binary_model = HybridClassifier(
        num_numeric=len(feature_cols),
        vocab_size=len(vocab),
        num_sources=len(source_map),
        num_transports=len(transport_map),
        num_classes=len(binary_label_names),
        hidden_dim=args.hidden_dim,
        seq_embedding_dim=args.seq_embedding_dim,
        source_embedding_dim=args.source_embedding_dim,
        transport_embedding_dim=args.transport_embedding_dim,
        dropout=args.dropout,
    ).to(device)

    binary_class_weights = compute_class_weight_tensor(
        binary_train_ds.label_ids,
        device=device,
        power=args.binary_class_weight_power,
    )
    binary_criterion = nn.CrossEntropyLoss(weight=binary_class_weights, label_smoothing=args.label_smoothing)
    binary_optimizer = torch.optim.AdamW(
        binary_model.parameters(),
        lr=args.binary_learning_rate,
        weight_decay=args.weight_decay,
    )
    binary_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        binary_optimizer,
        mode="max",
        factor=0.5,
        patience=args.scheduler_patience,
        min_lr=args.min_learning_rate,
    )

    binary_history, binary_best_state, binary_best_epoch, binary_best_val_metrics = train_stage(
        model=binary_model,
        train_loader=binary_train_loader,
        valid_loader=binary_valid_loader,
        optimizer=binary_optimizer,
        scheduler=binary_scheduler,
        criterion=binary_criterion,
        device=device,
        epochs=args.binary_epochs,
        grad_clip=args.grad_clip,
        early_stop_patience=args.early_stop_patience,
    )
    binary_model.load_state_dict(binary_best_state)
    binary_test_metrics, binary_y_true, binary_y_pred, binary_sources = evaluate(
        binary_model,
        binary_test_loader,
        binary_criterion,
        device,
    )
    pd.DataFrame(binary_history).to_csv(output_dir / "binary_history.csv", index=False)
    binary_output_dir = output_dir / "binary_artifacts"
    multiclass_output_dir = output_dir / "multiclass_artifacts"
    binary_output_dir.mkdir(parents=True, exist_ok=True)
    multiclass_output_dir.mkdir(parents=True, exist_ok=True)

    binary_report = save_report_artifacts(
        output_dir=binary_output_dir,
        label_names=binary_label_names,
        y_true=binary_y_true,
        y_pred=binary_y_pred,
        source_names=binary_sources,
    )

    multiclass_model = HybridClassifier(
        num_numeric=len(feature_cols),
        vocab_size=len(vocab),
        num_sources=len(source_map),
        num_transports=len(transport_map),
        num_classes=len(multiclass_label_names),
        hidden_dim=args.hidden_dim,
        seq_embedding_dim=args.seq_embedding_dim,
        source_embedding_dim=args.source_embedding_dim,
        transport_embedding_dim=args.transport_embedding_dim,
        dropout=args.dropout,
    ).to(device)
    transfer_encoder_weights(binary_model, multiclass_model)

    multiclass_class_weights = compute_class_weight_tensor(
        multiclass_train_ds.label_ids,
        device=device,
        power=args.multiclass_class_weight_power,
    )
    multiclass_criterion = nn.CrossEntropyLoss(
        weight=multiclass_class_weights,
        label_smoothing=args.label_smoothing,
    )
    multiclass_optimizer = torch.optim.AdamW(
        multiclass_model.parameters(),
        lr=args.multiclass_learning_rate,
        weight_decay=args.weight_decay,
    )
    multiclass_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        multiclass_optimizer,
        mode="max",
        factor=0.5,
        patience=args.scheduler_patience,
        min_lr=args.min_learning_rate,
    )

    multiclass_history, multiclass_best_state, multiclass_best_epoch, multiclass_best_val_metrics = train_stage(
        model=multiclass_model,
        train_loader=multiclass_train_loader,
        valid_loader=multiclass_valid_loader,
        optimizer=multiclass_optimizer,
        scheduler=multiclass_scheduler,
        criterion=multiclass_criterion,
        device=device,
        epochs=args.multiclass_epochs,
        grad_clip=args.grad_clip,
        early_stop_patience=args.early_stop_patience,
    )
    multiclass_model.load_state_dict(multiclass_best_state)
    multiclass_test_metrics, multiclass_y_true, multiclass_y_pred, multiclass_sources = evaluate(
        multiclass_model,
        multiclass_test_loader,
        multiclass_criterion,
        device,
    )
    pd.DataFrame(multiclass_history).to_csv(output_dir / "multiclass_history.csv", index=False)
    multiclass_report = save_report_artifacts(
        output_dir=multiclass_output_dir,
        label_names=multiclass_label_names,
        y_true=multiclass_y_true,
        y_pred=multiclass_y_pred,
        source_names=multiclass_sources,
    )

    full_label_names = list(metadata["final_label_order"])
    full_label_map = make_label_map(full_label_names)
    binary_predictions_full = predict_classes(binary_model, multiclass_test_full_binary_loader, device=device)
    encrypted_prediction_indices = np.where(binary_predictions_full == binary_label_map["ENCRYPTED"])[0]

    final_predictions_text = np.full(len(multiclass_test_full), "NON_ENCRYPTED", dtype=object)
    if len(encrypted_prediction_indices) > 0:
        encrypted_subset = multiclass_test_full.iloc[encrypted_prediction_indices].copy()
        encrypted_subset["label"] = encrypted_subset["final_label"].astype(str)
        encrypted_subset_ds = HybridDataset(
            frame=encrypted_subset,
            feature_cols=feature_cols,
            preprocessor=preprocessor,
            vocab=vocab,
            source_map=source_map,
            transport_map=transport_map,
            label_map=None,
            max_seq_len=args.max_seq_len,
        )
        encrypted_subset_loader = build_loader(
            encrypted_subset_ds,
            batch_size=args.batch_size,
            weighted=False,
            shuffle=False,
        )
        encrypted_predictions = predict_classes(multiclass_model, encrypted_subset_loader, device=device)
        final_predictions_text[encrypted_prediction_indices] = [
            multiclass_label_names[index] for index in encrypted_predictions
        ]

    final_y_true = multiclass_test_full["final_label"].map(full_label_map).to_numpy(dtype=np.int64)
    final_y_pred = np.asarray([full_label_map[label] for label in final_predictions_text], dtype=np.int64)
    hierarchical_output_dir = output_dir / "hierarchical_artifacts"
    hierarchical_report = save_report_artifacts(
        output_dir=hierarchical_output_dir,
        label_names=full_label_names,
        y_true=final_y_true,
        y_pred=final_y_pred,
        source_names=multiclass_test_full["source_name"].astype(str).tolist(),
    )
    hierarchical_test_metrics = {
        "accuracy": float(accuracy_score(final_y_true, final_y_pred)),
        "f1_macro": float(f1_score(final_y_true, final_y_pred, average="macro")),
        "f1_weighted": float(f1_score(final_y_true, final_y_pred, average="weighted")),
    }

    artifact_bundle = {
        "feature_cols": feature_cols,
        "vocab": vocab,
        "source_map": source_map,
        "transport_map": transport_map,
        "binary_label_map": binary_label_map,
        "multiclass_label_map": multiclass_label_map,
        "numeric_preprocessor": preprocessor.to_dict(feature_cols),
        "config": vars(args),
    }
    (output_dir / "artifacts.json").write_text(json.dumps(artifact_bundle, indent=2, ensure_ascii=False), encoding="utf-8")

    torch.save(
        {
            "binary_state_dict": binary_model.state_dict(),
            "multiclass_state_dict": multiclass_model.state_dict(),
            "artifacts": artifact_bundle,
        },
        output_dir / "hybrid_model.pt",
    )

    metrics = {
        "device": str(device),
        "binary_pretrain": {
            "samples_train": int(len(binary_train_ds)),
            "samples_valid": int(len(binary_valid_ds)),
            "samples_test": int(len(binary_test_ds)),
            "epochs_requested": int(args.binary_epochs),
            "epochs_trained": int(len(binary_history)),
            "best_epoch": int(binary_best_epoch),
            "learning_rate": float(args.binary_learning_rate),
            "weight_decay": float(args.weight_decay),
            "sampler_power": float(args.binary_sampler_power),
            "class_weight_power": float(args.binary_class_weight_power),
            "best_val_metrics": binary_best_val_metrics,
            "test_metrics": binary_test_metrics,
            "class_recalls": binary_report["class_recalls"],
        },
        "multiclass_finetune": {
            "samples_train": int(len(multiclass_train_ds)),
            "samples_valid": int(len(multiclass_valid_ds)),
            "samples_test": int(len(multiclass_test_ds)),
            "label_names": multiclass_label_names,
            "epochs_requested": int(args.multiclass_epochs),
            "epochs_trained": int(len(multiclass_history)),
            "best_epoch": int(multiclass_best_epoch),
            "learning_rate": float(args.multiclass_learning_rate),
            "weight_decay": float(args.weight_decay),
            "sampler_power": float(args.multiclass_sampler_power),
            "class_weight_power": float(args.multiclass_class_weight_power),
            "best_val_metrics": multiclass_best_val_metrics,
            "test_metrics": multiclass_test_metrics,
            "class_recalls": multiclass_report["class_recalls"],
        },
        "hierarchical_final": {
            "samples_test": int(len(multiclass_test_full)),
            "label_names": full_label_names,
            "test_metrics": hierarchical_test_metrics,
            "class_recalls": hierarchical_report["class_recalls"],
        },
    }
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Hybrid training complete.")
    print(f"Device             : {device}")
    print(f"Binary test Acc    : {binary_test_metrics['accuracy']:.4f}")
    print(f"Binary test MacroF1: {binary_test_metrics['f1_macro']:.4f}")
    print(f"Enc-only Acc       : {multiclass_test_metrics['accuracy']:.4f}")
    print(f"Enc-only MacroF1   : {multiclass_test_metrics['f1_macro']:.4f}")
    print(f"Final test Acc     : {hierarchical_test_metrics['accuracy']:.4f}")
    print(f"Final test MacroF1 : {hierarchical_test_metrics['f1_macro']:.4f}")
    print(f"Metrics            : {metrics_path}")
    print(f"Model              : {output_dir / 'hybrid_model.pt'}")


if __name__ == "__main__":
    main()
