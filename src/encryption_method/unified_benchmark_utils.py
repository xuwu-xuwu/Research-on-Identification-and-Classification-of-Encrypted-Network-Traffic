#!/usr/bin/env python
"""Shared helpers for fair encryption-method benchmark experiments.

These helpers intentionally avoid `source_name` as an input feature because the
current unified dataset is highly source-coupled and source identifiers would
introduce strong dataset-origin leakage into the main comparison table.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score


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

MULTICLASS_FILENAME = "multiclass_finetune.csv"
METADATA_FILENAME = "metadata.json"


def safe_log1p(values: np.ndarray) -> np.ndarray:
    return np.sign(values) * np.log1p(np.abs(values))


@dataclass
class SplitFrames:
    train: pd.DataFrame
    valid: pd.DataFrame
    test: pd.DataFrame
    label_names: list[str]


def load_multiclass_splits(data_dir: str | Path) -> SplitFrames:
    data_dir = Path(data_dir)
    csv_path = data_dir / MULTICLASS_FILENAME
    if not csv_path.exists():
        raise FileNotFoundError(f"Unified multiclass csv not found: {csv_path}")

    df = pd.read_csv(csv_path, low_memory=False)
    required_columns = {"split", "final_label", "transport"}
    missing_columns = sorted(required_columns - set(df.columns))
    if missing_columns:
        raise ValueError(f"Unified dataset is missing required columns: {missing_columns}")

    metadata_path = data_dir / METADATA_FILENAME
    label_names: list[str]
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        label_names = list(metadata.get("final_label_order", []))
    else:
        label_names = []

    if not label_names:
        label_names = sorted(df["final_label"].dropna().astype(str).unique().tolist())

    available_labels = set(df["final_label"].dropna().astype(str))
    label_names = [label for label in label_names if label in available_labels]

    train = df.loc[df["split"] == "train"].reset_index(drop=True)
    valid = df.loc[df["split"] == "valid"].reset_index(drop=True)
    test = df.loc[df["split"] == "test"].reset_index(drop=True)

    if train.empty or valid.empty or test.empty:
        raise ValueError("Unified dataset split columns do not contain non-empty train/valid/test partitions.")

    return SplitFrames(train=train, valid=valid, test=test, label_names=label_names)


class UnifiedTabularPreprocessor:
    """Median-impute, signed-log-scale, standardize, and optionally append transport one-hot."""

    def __init__(self, include_transport: bool = True) -> None:
        self.include_transport = include_transport
        self.feature_cols = list(COMMON_NUMERIC_FEATURES)
        self.transport_categories: list[str] = []
        self.medians: np.ndarray | None = None
        self.means: np.ndarray | None = None
        self.stds: np.ndarray | None = None

    def fit(self, frame: pd.DataFrame) -> "UnifiedTabularPreprocessor":
        numeric = frame[self.feature_cols].to_numpy(dtype=np.float32, copy=True)
        medians = np.nanmedian(numeric, axis=0)
        medians = np.where(np.isnan(medians), 0.0, medians)
        filled = np.where(np.isnan(numeric), medians, numeric)
        logged = safe_log1p(filled)
        means = logged.mean(axis=0)
        stds = logged.std(axis=0)
        stds = np.where(stds < 1e-6, 1.0, stds)

        self.medians = medians.astype(np.float32)
        self.means = means.astype(np.float32)
        self.stds = stds.astype(np.float32)

        if self.include_transport:
            transport_series = frame["transport"].fillna("OTHER").astype(str).str.upper()
            self.transport_categories = sorted(transport_series.unique().tolist())

        return self

    def _encode_numeric(self, frame: pd.DataFrame) -> np.ndarray:
        if self.medians is None or self.means is None or self.stds is None:
            raise RuntimeError("Preprocessor must be fit before transform.")

        numeric = frame[self.feature_cols].to_numpy(dtype=np.float32, copy=True)
        filled = np.where(np.isnan(numeric), self.medians, numeric)
        logged = safe_log1p(filled)
        normalized = (logged - self.means) / self.stds
        return normalized.astype(np.float32)

    def _encode_transport(self, frame: pd.DataFrame) -> np.ndarray:
        if not self.include_transport:
            return np.zeros((len(frame), 0), dtype=np.float32)
        if not self.transport_categories:
            raise RuntimeError("Transport categories are not initialized.")

        transport_series = frame["transport"].fillna("OTHER").astype(str).str.upper()
        matrix = np.zeros((len(frame), len(self.transport_categories)), dtype=np.float32)
        category_to_index = {category: index for index, category in enumerate(self.transport_categories)}
        for row_index, category in enumerate(transport_series):
            column_index = category_to_index.get(category)
            if column_index is not None:
                matrix[row_index, column_index] = 1.0
        return matrix

    def transform(self, frame: pd.DataFrame) -> np.ndarray:
        numeric = self._encode_numeric(frame)
        transport = self._encode_transport(frame)
        if transport.shape[1] == 0:
            return numeric
        return np.concatenate([numeric, transport], axis=1)

    def metadata(self) -> dict[str, object]:
        return {
            "feature_cols": self.feature_cols,
            "include_transport": self.include_transport,
            "transport_categories": self.transport_categories,
            "output_dim": len(self.feature_cols) + len(self.transport_categories),
        }


def encode_labels(labels: pd.Series, label_names: list[str]) -> np.ndarray:
    label_to_id = {label: index for index, label in enumerate(label_names)}
    unknown = sorted(set(labels.astype(str)) - set(label_to_id))
    if unknown:
        raise ValueError(f"Encountered labels not present in label_names: {unknown}")
    return labels.astype(str).map(label_to_id).to_numpy(dtype=np.int64)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, label_names: list[str]) -> dict[str, object]:
    label_ids = np.arange(len(label_names), dtype=np.int64)
    report_dict = classification_report(
        y_true,
        y_pred,
        labels=label_ids,
        target_names=label_names,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    report_text = classification_report(
        y_true,
        y_pred,
        labels=label_ids,
        target_names=label_names,
        digits=4,
        zero_division=0,
    )
    confusion = confusion_matrix(y_true, y_pred, labels=label_ids)

    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
        "macro_recall": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
        "class_recalls": {
            label: float(recall_score(y_true == label_id, y_pred == label_id, zero_division=0))
            for label_id, label in enumerate(label_names)
        },
        "classification_report": report_dict,
        "classification_report_text": report_text,
        "confusion_matrix": confusion.tolist(),
    }
    return metrics


def write_metrics_bundle(output_dir: str | Path, bundle: dict[str, object], label_names: list[str]) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_text = str(bundle.pop("classification_report_text"))
    report_dict = bundle["classification_report"]
    confusion = bundle["confusion_matrix"]

    (output_dir / "metrics.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    pd.DataFrame(report_dict).transpose().to_csv(output_dir / "classification_report.csv", index=True)
    pd.DataFrame(confusion, index=label_names, columns=label_names).to_csv(output_dir / "confusion_matrix.csv")
