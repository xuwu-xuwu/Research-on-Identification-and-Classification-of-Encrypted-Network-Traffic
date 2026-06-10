#!/usr/bin/env python
"""Train the current full-data enhanced fusion method.

This is the full 9-class counterpart of the PCAP fusion method. Most rows in
the unified full dataset do not have raw packet bytes, so this model uses the
full-data-safe fusion inputs:

- flow-level numeric statistics
- transport one-hot features
- sequence-derived statistics when `sequence_text` is available

`source_name` is intentionally excluded to avoid dataset-origin leakage.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.encryption_method.unified_benchmark_utils import (  # noqa: E402
    COMMON_NUMERIC_FEATURES,
    compute_metrics,
    encode_labels,
    safe_log1p,
    write_metrics_bundle,
)


@dataclass
class FullFusionPreprocessor:
    numeric_medians: np.ndarray
    numeric_means: np.ndarray
    numeric_stds: np.ndarray
    sequence_means: np.ndarray
    sequence_stds: np.ndarray
    transport_categories: list[str]

    @classmethod
    def fit(cls, frame: pd.DataFrame) -> "FullFusionPreprocessor":
        numeric_raw = frame[COMMON_NUMERIC_FEATURES].to_numpy(dtype=np.float32, copy=True)
        medians = np.nanmedian(numeric_raw, axis=0)
        medians = np.where(np.isnan(medians), 0.0, medians)
        numeric_filled = np.where(np.isnan(numeric_raw), medians, numeric_raw)
        numeric_logged = safe_log1p(numeric_filled)
        numeric_means = numeric_logged.mean(axis=0)
        numeric_stds = numeric_logged.std(axis=0)
        numeric_stds = np.where(numeric_stds < 1e-6, 1.0, numeric_stds)

        sequence_raw = extract_sequence_features(frame["sequence_text"].fillna("").astype(str).to_numpy())
        sequence_logged = sequence_raw.copy()
        sequence_logged[:, 1:] = safe_log1p(sequence_logged[:, 1:])
        sequence_means = sequence_logged.mean(axis=0)
        sequence_stds = sequence_logged.std(axis=0)
        sequence_stds = np.where(sequence_stds < 1e-6, 1.0, sequence_stds)

        transport_categories = sorted(frame["transport"].fillna("OTHER").astype(str).str.upper().unique().tolist())
        return cls(
            numeric_medians=medians.astype(np.float32),
            numeric_means=numeric_means.astype(np.float32),
            numeric_stds=numeric_stds.astype(np.float32),
            sequence_means=sequence_means.astype(np.float32),
            sequence_stds=sequence_stds.astype(np.float32),
            transport_categories=transport_categories,
        )

    def transform(self, frame: pd.DataFrame) -> np.ndarray:
        numeric_raw = frame[COMMON_NUMERIC_FEATURES].to_numpy(dtype=np.float32, copy=True)
        numeric_filled = np.where(np.isnan(numeric_raw), self.numeric_medians, numeric_raw)
        numeric_logged = safe_log1p(numeric_filled)
        numeric = ((numeric_logged - self.numeric_means) / self.numeric_stds).astype(np.float32)

        transport = encode_transport(frame["transport"].fillna("OTHER").astype(str).str.upper().to_numpy(), self.transport_categories)

        sequence = extract_sequence_features(frame["sequence_text"].fillna("").astype(str).to_numpy())
        sequence[:, 1:] = safe_log1p(sequence[:, 1:])
        sequence = ((sequence - self.sequence_means) / self.sequence_stds).astype(np.float32)

        return np.concatenate([numeric, transport, sequence], axis=1).astype(np.float32, copy=False)

    def to_dict(self) -> dict[str, object]:
        return {
            "numeric_features": COMMON_NUMERIC_FEATURES,
            "numeric_medians": self.numeric_medians.tolist(),
            "numeric_means": self.numeric_means.tolist(),
            "numeric_stds": self.numeric_stds.tolist(),
            "transport_categories": self.transport_categories,
            "sequence_features": SEQUENCE_FEATURE_NAMES,
            "sequence_means": self.sequence_means.tolist(),
            "sequence_stds": self.sequence_stds.tolist(),
            "feature_blocks": {
                "numeric": len(COMMON_NUMERIC_FEATURES),
                "transport": len(self.transport_categories),
                "sequence_derived": len(SEQUENCE_FEATURE_NAMES),
            },
            "feature_dim": len(COMMON_NUMERIC_FEATURES) + len(self.transport_categories) + len(SEQUENCE_FEATURE_NAMES),
            "source_name_excluded": True,
        }


SEQUENCE_FEATURE_NAMES = [
    "has_sequence",
    "token_count",
    "packet_token_count",
    "fwd_packet_tokens",
    "bwd_packet_tokens",
    "direction_packet_ratio",
    "mean_len_bucket",
    "std_len_bucket",
    "min_len_bucket",
    "max_len_bucket",
    "mean_fwd_len_bucket",
    "mean_bwd_len_bucket",
    "mean_iat_bucket",
    "std_iat_bucket",
    "min_iat_bucket",
    "max_iat_bucket",
    "direction_byte_ratio",
    "iat_token_count",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train full-data enhanced fusion model for encryption-method identification.")
    parser.add_argument(
        "--data-dir",
        default="data/unified_encryption_method_v2_all_data",
        help="Directory containing multiclass_finetune.csv and metadata.json.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/encryption_method/full_enhanced_fusion_v1",
        help="Output directory.",
    )
    parser.add_argument("--n-estimators", type=int, default=350, help="XGBoost estimator count.")
    parser.add_argument("--max-depth", type=int, default=7, help="XGBoost tree depth.")
    parser.add_argument("--learning-rate", type=float, default=0.05, help="XGBoost learning rate.")
    parser.add_argument("--subsample", type=float, default=0.85, help="XGBoost subsample.")
    parser.add_argument("--colsample-bytree", type=float, default=0.85, help="XGBoost column subsample.")
    parser.add_argument("--min-child-weight", type=float, default=2.0, help="XGBoost min child weight.")
    parser.add_argument(
        "--class-weight-power",
        type=float,
        default=0.5,
        help="Power for inverse-frequency sample weights. 0 disables weighting.",
    )
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--n-jobs", type=int, default=-1, help="Parallel jobs for XGBoost.")
    return parser.parse_args()


def parse_bucket_suffix(token: str) -> float | None:
    try:
        return float(token.rsplit("_", 1)[1])
    except (IndexError, ValueError):
        return None


def extract_sequence_features(texts: np.ndarray) -> np.ndarray:
    features = np.zeros((len(texts), len(SEQUENCE_FEATURE_NAMES)), dtype=np.float32)
    for row_index, text in enumerate(texts):
        if not text.strip():
            continue

        fwd_lengths: list[float] = []
        bwd_lengths: list[float] = []
        iats: list[float] = []
        tokens = text.split()
        for token in tokens:
            if token.startswith("F_LEN_"):
                value = parse_bucket_suffix(token)
                if value is not None:
                    fwd_lengths.append(value)
            elif token.startswith("B_LEN_"):
                value = parse_bucket_suffix(token)
                if value is not None:
                    bwd_lengths.append(value)
            elif token.startswith("IAT_"):
                value = parse_bucket_suffix(token)
                if value is not None:
                    iats.append(value)

        all_lengths = np.asarray(fwd_lengths + bwd_lengths, dtype=np.float32)
        fwd = np.asarray(fwd_lengths, dtype=np.float32)
        bwd = np.asarray(bwd_lengths, dtype=np.float32)
        iat_values = np.asarray(iats, dtype=np.float32)

        features[row_index, 0] = 1.0
        features[row_index, 1] = len(tokens)
        features[row_index, 2] = len(fwd_lengths) + len(bwd_lengths)
        features[row_index, 3] = len(fwd_lengths)
        features[row_index, 4] = len(bwd_lengths)
        features[row_index, 5] = len(fwd_lengths) / (len(bwd_lengths) + 1.0)
        if all_lengths.size:
            features[row_index, 6] = float(all_lengths.mean())
            features[row_index, 7] = float(all_lengths.std())
            features[row_index, 8] = float(all_lengths.min())
            features[row_index, 9] = float(all_lengths.max())
        if fwd.size:
            features[row_index, 10] = float(fwd.mean())
        if bwd.size:
            features[row_index, 11] = float(bwd.mean())
        if iat_values.size:
            features[row_index, 12] = float(iat_values.mean())
            features[row_index, 13] = float(iat_values.std())
            features[row_index, 14] = float(iat_values.min())
            features[row_index, 15] = float(iat_values.max())
        features[row_index, 16] = float(fwd.sum() / (bwd.sum() + 1.0)) if (fwd.size or bwd.size) else 0.0
        features[row_index, 17] = len(iats)
    return features


def encode_transport(values: np.ndarray, categories: list[str]) -> np.ndarray:
    matrix = np.zeros((len(values), len(categories)), dtype=np.float32)
    category_to_index = {category: index for index, category in enumerate(categories)}
    for row_index, value in enumerate(values):
        column_index = category_to_index.get(str(value).upper())
        if column_index is not None:
            matrix[row_index, column_index] = 1.0
    return matrix


def sample_weights(y_train: np.ndarray, num_classes: int, power: float) -> np.ndarray | None:
    if power <= 0:
        return None
    counts = np.bincount(y_train, minlength=num_classes).astype(np.float32)
    base = counts.sum() / (np.maximum(counts, 1.0) * num_classes)
    weights = np.power(base, power)
    return weights[y_train].astype(np.float32, copy=False)


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "multiclass_finetune.csv"
    metadata_path = data_dir / "metadata.json"
    if not csv_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(f"Required full-data files not found under {data_dir}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    label_names = list(metadata["final_label_order"])
    usecols = ["split", "final_label", "transport", "sequence_text"] + COMMON_NUMERIC_FEATURES
    frame = pd.read_csv(csv_path, usecols=usecols, low_memory=False)

    train_frame = frame.loc[frame["split"] == "train"].copy()
    valid_frame = frame.loc[frame["split"] == "valid"].copy()
    test_frame = frame.loc[frame["split"] == "test"].copy()
    if train_frame.empty or valid_frame.empty or test_frame.empty:
        raise ValueError("Full dataset split must include non-empty train/valid/test partitions.")

    preprocessor = FullFusionPreprocessor.fit(train_frame)
    x_train = preprocessor.transform(train_frame)
    x_valid = preprocessor.transform(valid_frame)
    x_test = preprocessor.transform(test_frame)

    y_train = encode_labels(train_frame["final_label"], label_names)
    y_valid = encode_labels(valid_frame["final_label"], label_names)
    y_test = encode_labels(test_frame["final_label"], label_names)
    weights = sample_weights(y_train, num_classes=len(label_names), power=args.class_weight_power)

    model = xgb.XGBClassifier(
        objective="multi:softprob",
        num_class=len(label_names),
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        subsample=args.subsample,
        colsample_bytree=args.colsample_bytree,
        min_child_weight=args.min_child_weight,
        reg_lambda=1.0,
        random_state=args.random_state,
        n_jobs=args.n_jobs,
        tree_method="hist",
        eval_metric="mlogloss",
    )
    model.fit(
        x_train,
        y_train,
        sample_weight=weights,
        eval_set=[(x_valid, y_valid)],
        verbose=False,
    )

    y_pred = model.predict(x_test)
    metrics = compute_metrics(y_test, y_pred, label_names=label_names)
    metrics.update(
        {
            "model_name": "full_enhanced_fusion_xgboost",
            "method_description": "full-data fusion of flow statistics, transport, and sequence-derived features",
            "data_dir": str(data_dir),
            "samples_train": int(len(train_frame)),
            "samples_valid": int(len(valid_frame)),
            "samples_test": int(len(test_frame)),
            "num_features": int(x_train.shape[1]),
            "source_name_excluded": True,
            "class_weight_power": float(args.class_weight_power),
            "xgboost_params": {
                "n_estimators": int(args.n_estimators),
                "max_depth": int(args.max_depth),
                "learning_rate": float(args.learning_rate),
                "subsample": float(args.subsample),
                "colsample_bytree": float(args.colsample_bytree),
                "min_child_weight": float(args.min_child_weight),
                "random_state": int(args.random_state),
            },
        }
    )

    write_metrics_bundle(output_dir, dict(metrics), label_names=label_names)
    model.save_model(output_dir / "model.json")
    joblib.dump(model, output_dir / "model.joblib")
    np.savez_compressed(output_dir / "predictions.npz", y_true=y_test, y_pred=y_pred)
    (output_dir / "feature_metadata.json").write_text(
        json.dumps(preprocessor.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary = pd.DataFrame(
        [
            {
                "model_name": metrics["model_name"],
                "accuracy": metrics["accuracy"],
                "f1_macro": metrics["f1_macro"],
                "f1_weighted": metrics["f1_weighted"],
                "macro_recall": metrics["macro_recall"],
                "num_features": metrics["num_features"],
            }
        ]
    )
    summary.to_csv(output_dir / "comparison.csv", index=False)
    markdown = [
        "# Full-Data Enhanced Fusion Method",
        "",
        f"- Data dir: `{data_dir}`",
        "- Source leakage guard: `source_name` excluded",
        "- Feature fusion: flow statistics + transport + sequence-derived statistics",
        "",
        summary.to_markdown(index=False),
        "",
    ]
    (output_dir / "comparison.md").write_text("\n".join(markdown), encoding="utf-8")

    print("Full enhanced fusion training finished.")
    print(f"Accuracy   : {metrics['accuracy']:.6f}")
    print(f"Macro-F1   : {metrics['f1_macro']:.6f}")
    print(f"Weighted-F1: {metrics['f1_weighted']:.6f}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
