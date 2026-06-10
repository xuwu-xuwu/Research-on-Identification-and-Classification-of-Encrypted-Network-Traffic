#!/usr/bin/env python
"""Train an independent deep-learning baseline on the flow-level ARFF/CSV dataset.

This script does not touch the existing baseline or optimized outputs.
It trains a tabular MLP on the current flow-level feature dataset and writes
all artifacts to a dedicated output directory.
"""

from __future__ import annotations

import argparse
import copy
import json
import random
import re
from pathlib import Path
from typing import Iterable

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def _strip_trailing_commas(text: str) -> str:
    return re.sub(r",+\s*$", "", text)


def load_arff(path: Path) -> pd.DataFrame:
    attributes: list[str] = []
    rows: list[list[str | None]] = []
    in_data = False

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("%"):
                continue

            lower = line.lower()
            if not in_data:
                if lower.startswith("@attribute"):
                    cleaned = _strip_trailing_commas(line)
                    match = re.match(
                        r"@attribute\s+('[^']+'|\"[^\"]+\"|[^\s,]+)\s+(.+)$",
                        cleaned,
                        flags=re.IGNORECASE,
                    )
                    if match:
                        attributes.append(match.group(1).strip("'\""))
                elif lower.startswith("@data"):
                    in_data = True
                continue

            cleaned = _strip_trailing_commas(line)
            parts = [part.strip() for part in cleaned.split(",")]
            if len(parts) < len(attributes):
                parts.extend([None] * (len(attributes) - len(parts)))
            elif len(parts) > len(attributes):
                parts = parts[: len(attributes)]
            rows.append(parts)

    if not attributes:
        raise ValueError(f"No attributes parsed from ARFF: {path}")
    if not rows:
        raise ValueError(f"No data rows parsed from ARFF: {path}")

    return pd.DataFrame(rows, columns=attributes)


def load_dataset(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".arff":
        return load_arff(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type: {suffix}. Use .arff or .csv")


def infer_label_column(columns: Iterable[str]) -> str:
    col_list = list(columns)
    preferred = ("class1", "class", "label", "target")
    lower_map = {col.lower(): col for col in col_list}
    for candidate in preferred:
        if candidate in lower_map:
            return lower_map[candidate]
    return col_list[-1]


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


def safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / (denominator.abs() + 1.0)


def add_ratio_feature(df: pd.DataFrame, left: str, right: str, output: str) -> None:
    if left in df.columns and right in df.columns:
        df[output] = safe_div(df[left], df[right])


def add_log_feature(df: pd.DataFrame, source: str, output: str) -> None:
    if source in df.columns:
        df[output] = np.log1p(df[source].clip(lower=0))


class TabularFeaturePreprocessor:
    def __init__(self, corr_threshold: float = 0.995, quantile_cap: float = 0.999) -> None:
        self.corr_threshold = corr_threshold
        self.quantile_cap = quantile_cap
        self.original_feature_cols: list[str] = []
        self.all_nan_cols: list[str] = []
        self.negative_missing_cols: list[str] = []
        self.nan_flag_cols: list[str] = []
        self.constant_cols: list[str] = []
        self.correlation_dropped_cols: list[str] = []
        self.fill_values: dict[str, float] = {}
        self.clip_upper: dict[str, float] = {}
        self.feature_cols: list[str] = []
        self.scaler = StandardScaler()

    def _convert_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce")
        return result.replace([np.inf, -np.inf], np.nan)

    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        feature_df = df.copy()

        add_ratio_feature(feature_df, "total_fiat", "total_biat", "total_iat_ratio")
        add_ratio_feature(feature_df, "mean_fiat", "mean_biat", "mean_iat_ratio")
        add_ratio_feature(feature_df, "min_fiat", "max_fiat", "fiat_minmax_ratio")
        add_ratio_feature(feature_df, "min_biat", "max_biat", "biat_minmax_ratio")
        add_ratio_feature(feature_df, "min_flowiat", "max_flowiat", "flowiat_minmax_ratio")
        add_ratio_feature(feature_df, "min_active", "max_active", "active_minmax_ratio")
        add_ratio_feature(feature_df, "min_idle", "max_idle", "idle_minmax_ratio")
        add_ratio_feature(feature_df, "mean_active", "mean_idle", "active_idle_ratio")
        add_ratio_feature(feature_df, "flowBytesPerSecond", "flowPktsPerSecond", "bytes_per_packet")
        add_ratio_feature(feature_df, "std_flowiat", "mean_flowiat", "flowiat_cv")
        add_ratio_feature(feature_df, "std_active", "mean_active", "active_cv")
        add_ratio_feature(feature_df, "std_idle", "mean_idle", "idle_cv")

        if {"max_fiat", "min_fiat"}.issubset(feature_df.columns):
            feature_df["fiat_range"] = feature_df["max_fiat"] - feature_df["min_fiat"]
        if {"max_biat", "min_biat"}.issubset(feature_df.columns):
            feature_df["biat_range"] = feature_df["max_biat"] - feature_df["min_biat"]
        if {"max_flowiat", "min_flowiat"}.issubset(feature_df.columns):
            feature_df["flowiat_range"] = feature_df["max_flowiat"] - feature_df["min_flowiat"]
        if {"max_active", "min_active"}.issubset(feature_df.columns):
            feature_df["active_range"] = feature_df["max_active"] - feature_df["min_active"]
        if {"max_idle", "min_idle"}.issubset(feature_df.columns):
            feature_df["idle_range"] = feature_df["max_idle"] - feature_df["min_idle"]

        if {"duration", "flowBytesPerSecond"}.issubset(feature_df.columns):
            feature_df["estimated_total_bytes"] = feature_df["duration"] * feature_df["flowBytesPerSecond"]
        if {"duration", "flowPktsPerSecond"}.issubset(feature_df.columns):
            feature_df["estimated_total_pkts"] = feature_df["duration"] * feature_df["flowPktsPerSecond"]
        if {"estimated_total_bytes", "estimated_total_pkts"}.issubset(feature_df.columns):
            feature_df["estimated_avg_pkt_bytes"] = safe_div(
                feature_df["estimated_total_bytes"], feature_df["estimated_total_pkts"]
            )

        add_log_feature(feature_df, "duration", "log_duration")
        add_log_feature(feature_df, "flowBytesPerSecond", "log_flow_bytes_per_second")
        add_log_feature(feature_df, "flowPktsPerSecond", "log_flow_pkts_per_second")
        add_log_feature(feature_df, "mean_flowiat", "log_mean_flowiat")
        add_log_feature(feature_df, "mean_active", "log_mean_active")
        add_log_feature(feature_df, "mean_idle", "log_mean_idle")
        add_log_feature(feature_df, "estimated_total_bytes", "log_estimated_total_bytes")
        add_log_feature(feature_df, "estimated_total_pkts", "log_estimated_total_pkts")

        return feature_df

    def fit(self, df: pd.DataFrame) -> "TabularFeaturePreprocessor":
        x = self._convert_numeric(df)
        self.original_feature_cols = x.columns.tolist()

        self.all_nan_cols = sorted(x.columns[x.isna().all()].tolist())
        if self.all_nan_cols:
            x = x.drop(columns=self.all_nan_cols)

        self.negative_missing_cols = sorted(
            [col for col in x.columns if pd.api.types.is_numeric_dtype(x[col]) and (x[col] < 0).any()]
        )
        for col in self.negative_missing_cols:
            x[f"{col}_is_missing"] = (x[col] < 0).astype(int)
            x.loc[x[col] < 0, col] = np.nan

        self.nan_flag_cols = sorted([col for col in x.columns if x[col].isna().any()])
        for col in self.nan_flag_cols:
            x[f"{col}_nan_flag"] = x[col].isna().astype(int)

        x = self._add_derived_features(x)

        for col in x.columns:
            median = x[col].median()
            if pd.isna(median):
                median = 0.0
            self.fill_values[col] = float(median)

        x = x.fillna(self.fill_values)

        for col in x.columns:
            upper = x[col].quantile(self.quantile_cap)
            if pd.isna(upper):
                upper = self.fill_values[col]
            self.clip_upper[col] = float(upper)
            x[col] = x[col].clip(upper=upper)

        self.constant_cols = sorted([col for col in x.columns if x[col].nunique(dropna=False) <= 1])
        if self.constant_cols:
            x = x.drop(columns=self.constant_cols)

        corr_matrix = x.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        self.correlation_dropped_cols = sorted(
            [col for col in upper.columns if any(upper[col] > self.corr_threshold)]
        )
        if self.correlation_dropped_cols:
            x = x.drop(columns=self.correlation_dropped_cols)

        self.feature_cols = x.columns.tolist()
        self.scaler.fit(x)
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        x = self._convert_numeric(df)

        for col in self.original_feature_cols:
            if col not in x.columns:
                x[col] = np.nan
        x = x[self.original_feature_cols]

        if self.all_nan_cols:
            x = x.drop(columns=[col for col in self.all_nan_cols if col in x.columns])

        for col in self.negative_missing_cols:
            if col not in x.columns:
                x[col] = np.nan
            x[f"{col}_is_missing"] = (x[col] < 0).astype(int)
            x.loc[x[col] < 0, col] = np.nan

        for col in self.nan_flag_cols:
            if col not in x.columns:
                x[col] = np.nan
            x[f"{col}_nan_flag"] = x[col].isna().astype(int)

        x = self._add_derived_features(x)

        for col in self.fill_values:
            if col not in x.columns:
                x[col] = np.nan
        x = x.reindex(columns=list(self.fill_values.keys()))

        for col, value in self.fill_values.items():
            x[col] = x[col].fillna(value)

        for col, upper in self.clip_upper.items():
            x[col] = x[col].clip(upper=upper)

        if self.constant_cols:
            x = x.drop(columns=[col for col in self.constant_cols if col in x.columns], errors="ignore")
        if self.correlation_dropped_cols:
            x = x.drop(columns=[col for col in self.correlation_dropped_cols if col in x.columns], errors="ignore")

        x = x.reindex(columns=self.feature_cols, fill_value=0.0)
        scaled = self.scaler.transform(x)
        return scaled.astype(np.float32, copy=False)

    def metadata(self) -> dict[str, object]:
        return {
            "all_nan_cols": self.all_nan_cols,
            "negative_missing_cols": self.negative_missing_cols,
            "nan_flag_cols": self.nan_flag_cols,
            "constant_cols": self.constant_cols,
            "correlation_dropped_cols": self.correlation_dropped_cols,
            "final_feature_cols": self.feature_cols,
        }


class FlowMLP(nn.Module):
    def __init__(self, input_dim: int, num_classes: int, hidden_dims: list[int], dropout: float) -> None:
        super().__init__()
        layers: list[nn.Module] = []
        current_dim = input_dim
        current_dropout = dropout

        for hidden_dim in hidden_dims:
            layers.extend(
                [
                    nn.Linear(current_dim, hidden_dim),
                    nn.BatchNorm1d(hidden_dim),
                    nn.GELU(),
                    nn.Dropout(current_dropout),
                ]
            )
            current_dim = hidden_dim
            current_dropout = max(0.05, current_dropout - 0.05)

        self.backbone = nn.Sequential(*layers)
        self.head = nn.Linear(current_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.backbone(x)
        return self.head(x)


def build_loader(features: np.ndarray, labels: np.ndarray, batch_size: int, shuffle: bool) -> DataLoader:
    dataset = TensorDataset(torch.from_numpy(features), torch.from_numpy(labels.astype(np.int64, copy=False)))
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,
        pin_memory=torch.cuda.is_available(),
    )


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
        for batch_x, batch_y in loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            logits = model(batch_x)
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
    fig_w = max(8, len(labels) * 0.8)
    fig_h = max(6, len(labels) * 0.65)
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
        title="Flow MLP Confusion Matrix",
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    threshold = cm.max() / 2.0 if cm.size else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                format(cm[i, j], "d"),
                ha="center",
                va="center",
                color="white" if cm[i, j] > threshold else "black",
                fontsize=8,
            )

    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a flow-level MLP classifier on ARFF/CSV data.")
    parser.add_argument("--data", required=True, help="Path to .arff or .csv dataset.")
    parser.add_argument("--label", default=None, help="Label column name. Auto-detected if omitted.")
    parser.add_argument("--output-dir", default="outputs/deep_learning/flow_mlp_v1", help="Directory for outputs.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split ratio.")
    parser.add_argument("--val-size", type=float, default=0.1, help="Validation ratio inside the development split.")
    parser.add_argument("--batch-size", type=int, default=256, help="Mini-batch size.")
    parser.add_argument("--epochs", type=int, default=120, help="Maximum number of epochs.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="AdamW learning rate.")
    parser.add_argument("--weight-decay", type=float, default=1e-4, help="AdamW weight decay.")
    parser.add_argument("--dropout", type=float, default=0.30, help="Initial dropout rate.")
    parser.add_argument("--hidden-dims", nargs="+", type=int, default=[256, 128, 64], help="Hidden layer widths.")
    parser.add_argument("--label-smoothing", type=float, default=0.02, help="CrossEntropy label smoothing.")
    parser.add_argument("--grad-clip", type=float, default=5.0, help="Gradient clipping threshold.")
    parser.add_argument("--scheduler-patience", type=int, default=8, help="ReduceLROnPlateau patience.")
    parser.add_argument("--early-stop-patience", type=int, default=20, help="Early stopping patience.")
    parser.add_argument("--min-learning-rate", type=float, default=1e-5, help="Scheduler lower bound.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    device = resolve_device(args.device)
    if hasattr(torch, "set_float32_matmul_precision"):
        torch.set_float32_matmul_precision("high")

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_dataset(data_path)
    if raw_df.empty:
        raise ValueError("Dataset is empty after loading.")

    label_column = args.label if args.label else infer_label_column(raw_df.columns)
    if label_column not in raw_df.columns:
        raise ValueError(f"Label column '{label_column}' not found.")

    y_raw = raw_df[label_column].astype(str).str.strip()
    valid_mask = (~y_raw.isna()) & (y_raw != "") & (y_raw != "?")
    df = raw_df.loc[valid_mask].copy()
    y_raw = y_raw.loc[valid_mask]
    source_indices = df.index.to_numpy()

    feature_df = df.drop(columns=[label_column]).copy()
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_raw.astype(str))
    class_names = label_encoder.classes_.tolist()

    positions = np.arange(len(feature_df))
    train_val_pos, test_pos = train_test_split(
        positions,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=y_encoded,
    )
    train_pos, val_pos = train_test_split(
        train_val_pos,
        test_size=args.val_size,
        random_state=args.seed,
        stratify=y_encoded[train_val_pos],
    )

    preprocessor = TabularFeaturePreprocessor()
    preprocessor.fit(feature_df.iloc[train_pos].copy())

    x_train = preprocessor.transform(feature_df.iloc[train_pos].copy())
    x_val = preprocessor.transform(feature_df.iloc[val_pos].copy())
    x_test = preprocessor.transform(feature_df.iloc[test_pos].copy())

    y_train = y_encoded[train_pos]
    y_val = y_encoded[val_pos]
    y_test = y_encoded[test_pos]

    train_loader = build_loader(x_train, y_train, args.batch_size, shuffle=True)
    val_loader = build_loader(x_val, y_val, args.batch_size, shuffle=False)
    test_loader = build_loader(x_test, y_test, args.batch_size, shuffle=False)

    class_counts = np.bincount(y_train, minlength=len(class_names))
    class_weights = class_counts.sum() / (len(class_names) * np.maximum(class_counts, 1))
    class_weights_tensor = torch.as_tensor(class_weights, dtype=torch.float32, device=device)

    model = FlowMLP(
        input_dim=x_train.shape[1],
        num_classes=len(class_names),
        hidden_dims=args.hidden_dims,
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

        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device, non_blocking=True)
            batch_y = batch_y.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            if args.grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            optimizer.step()
            train_losses.append(float(loss.item()))

        val_metrics, _, _, _ = evaluate(model, val_loader, criterion, device)
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
        target_names=class_names,
        digits=4,
        zero_division=0,
    )
    report_dict = classification_report(
        y_test_eval,
        test_pred,
        target_names=class_names,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    recalls = recall_score(y_test_eval, test_pred, average=None, zero_division=0)
    cm = confusion_matrix(y_test_eval, test_pred, labels=np.arange(len(class_names)))

    confidence = test_prob.max(axis=1)
    sorted_prob = np.sort(test_prob, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2] if test_prob.shape[1] > 1 else np.ones_like(confidence)
    prediction_df = pd.DataFrame(
        {
            "source_index": source_indices[test_pos],
            "y_true": [class_names[idx] for idx in y_test_eval],
            "y_pred": [class_names[idx] for idx in test_pred],
            "confidence": confidence,
            "margin_top1_top2": margin,
            "is_correct": y_test_eval == test_pred,
        }
    )

    metrics = {
        "data_path": str(data_path),
        "label_column": label_column,
        "samples_total": int(len(df)),
        "samples_train": int(len(train_pos)),
        "samples_val": int(len(val_pos)),
        "samples_test": int(len(test_pos)),
        "num_features": int(x_train.shape[1]),
        "num_classes": int(len(class_names)),
        "class_names": class_names,
        "hidden_dims": args.hidden_dims,
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
        "test_loss": float(test_metrics["loss"]),
        "accuracy": float(test_metrics["accuracy"]),
        "f1_macro": float(test_metrics["f1_macro"]),
        "f1_weighted": float(test_metrics["f1_weighted"]),
        "class_recalls": {name: float(value) for name, value in zip(class_names, recalls)},
        "best_val_metrics": best_val_metrics,
        "feature_metadata": preprocessor.metadata(),
    }

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    pd.DataFrame(report_dict).transpose().to_csv(output_dir / "classification_report.csv", index=True)
    pd.DataFrame(cm, index=class_names, columns=class_names).to_csv(output_dir / "confusion_matrix.csv")
    prediction_df.to_csv(output_dir / "test_predictions.csv", index=False)
    np.savez_compressed(
        output_dir / "splits.npz",
        train_source_index=source_indices[train_pos],
        val_source_index=source_indices[val_pos],
        test_source_index=source_indices[test_pos],
    )
    save_confusion_matrix(cm, class_names, output_dir / "confusion_matrix.png")
    joblib.dump(preprocessor, output_dir / "preprocessor.joblib")
    torch.save(
        {
            "state_dict": model.state_dict(),
            "model_type": "flow_mlp",
            "input_dim": int(x_train.shape[1]),
            "num_classes": int(len(class_names)),
            "hidden_dims": args.hidden_dims,
            "dropout": float(args.dropout),
            "class_names": class_names,
            "label_column": label_column,
            "metrics": metrics,
        },
        output_dir / "model.pt",
    )

    print("Deep-learning training finished.")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"F1 (macro) : {metrics['f1_macro']:.4f}")
    print(f"F1 (weight): {metrics['f1_weighted']:.4f}")
    print(f"Best epoch : {metrics['best_epoch']}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
