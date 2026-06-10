#!/usr/bin/env python
"""Minimal baseline trainer for encrypted traffic classification.

Supports ARFF/CSV input and trains a RandomForest model.
Outputs:
1) metrics.json
2) classification_report.txt
3) confusion_matrix.png
4) model.joblib

Example:
python src/baseline/train_baseline.py ^
  --data "data/Scenario B-ARFF/Scenario B-ARFF/TimeBasedFeatures-Dataset-15s-AllinOne.arff" ^
  --label class1
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


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
                        attr_name = match.group(1).strip("'\"")
                        attributes.append(attr_name)
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
        title="Confusion Matrix",
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Train RandomForest baseline on ARFF/CSV data.")
    parser.add_argument("--data", required=True, help="Path to .arff or .csv dataset.")
    parser.add_argument("--label", default=None, help="Label column name. Auto-detected if omitted.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split ratio.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--n-estimators", type=int, default=300, help="Number of trees.")
    parser.add_argument("--n-jobs", type=int, default=1, help="Parallel workers for RandomForest.")
    parser.add_argument("--output-dir", default="outputs/baseline", help="Directory for outputs.")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {data_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_dataset(data_path)
    if df.empty:
        raise ValueError("Dataset is empty after loading.")

    label_column = args.label if args.label else infer_label_column(df.columns)
    if label_column not in df.columns:
        raise ValueError(f"Label column '{label_column}' not found in dataset columns.")

    y = df[label_column].astype(str).str.strip()
    valid_mask = (~y.isna()) & (y != "") & (y != "?")
    df = df.loc[valid_mask].copy()
    y = y.loc[valid_mask]

    x = df.drop(columns=[label_column]).copy()
    for col in x.columns:
        x[col] = pd.to_numeric(x[col], errors="coerce")
    x = x.replace([np.inf, -np.inf], np.nan)

    empty_columns = x.columns[x.isna().all()].tolist()
    if empty_columns:
        x = x.drop(columns=empty_columns)

    if x.shape[1] == 0:
        raise ValueError("All feature columns are empty after numeric conversion.")
    if y.nunique() < 2:
        raise ValueError("Need at least 2 classes for classification.")

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "rf",
                RandomForestClassifier(
                    n_estimators=args.n_estimators,
                    random_state=args.random_state,
                    n_jobs=args.n_jobs,
                    class_weight="balanced",
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    metrics = {
        "data_path": str(data_path),
        "label_column": label_column,
        "samples_total": int(len(df)),
        "samples_train": int(len(x_train)),
        "samples_test": int(len(x_test)),
        "num_features": int(x.shape[1]),
        "num_classes": int(y.nunique()),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_test, y_pred, average="weighted")),
        "dropped_all_nan_columns": empty_columns,
    }

    labels = sorted(y.unique().tolist())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    report = classification_report(y_test, y_pred, digits=4)

    metrics_path = output_dir / "metrics.json"
    report_path = output_dir / "classification_report.txt"
    cm_path = output_dir / "confusion_matrix.png"
    model_path = output_dir / "model.joblib"

    model_bundle = {
        "model": model,
        "feature_columns": x.columns.tolist(),
        "label_column": label_column,
        "class_labels": labels,
        "data_path": str(data_path),
        "dropped_all_nan_columns": empty_columns,
    }

    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    report_path.write_text(report, encoding="utf-8")
    save_confusion_matrix(cm, labels, cm_path)
    joblib.dump(model_bundle, model_path)

    print("Training finished.")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"F1 (macro) : {metrics['f1_macro']:.4f}")
    print(f"F1 (weight): {metrics['f1_weighted']:.4f}")
    print(f"Metrics    : {metrics_path}")
    print(f"Report     : {report_path}")
    print(f"CM Figure  : {cm_path}")
    print(f"Model      : {model_path}")


if __name__ == "__main__":
    main()

