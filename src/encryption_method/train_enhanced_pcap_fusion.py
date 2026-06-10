#!/usr/bin/env python
"""Train an enhanced current-method baseline for the PCAP paper benchmark.

The original current hybrid model is designed for the full tabular main table.
On the small PCAP benchmark, its hierarchical binary-then-multiclass decision
adds error propagation. This script trains a single-stage 5-class fusion model
that keeps the current flow-statistic branch and adds packet-byte evidence.
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
from sklearn.ensemble import ExtraTreesClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.encryption_method.unified_benchmark_utils import (  # noqa: E402
    COMMON_NUMERIC_FEATURES,
    compute_metrics,
    safe_log1p,
    write_metrics_bundle,
)


@dataclass
class FusionPreprocessor:
    medians: np.ndarray
    means: np.ndarray
    stds: np.ndarray

    @classmethod
    def fit(cls, numeric_frame: pd.DataFrame) -> "FusionPreprocessor":
        values = numeric_frame[COMMON_NUMERIC_FEATURES].to_numpy(dtype=np.float32, copy=True)
        medians = np.nanmedian(values, axis=0)
        medians = np.where(np.isnan(medians), 0.0, medians)
        filled = np.where(np.isnan(values), medians, values)
        logged = safe_log1p(filled)
        means = logged.mean(axis=0)
        stds = logged.std(axis=0)
        stds = np.where(stds < 1e-6, 1.0, stds)
        return cls(
            medians=medians.astype(np.float32),
            means=means.astype(np.float32),
            stds=stds.astype(np.float32),
        )

    def transform_numeric(self, numeric_frame: pd.DataFrame) -> np.ndarray:
        values = numeric_frame[COMMON_NUMERIC_FEATURES].to_numpy(dtype=np.float32, copy=True)
        filled = np.where(np.isnan(values), self.medians, values)
        logged = safe_log1p(filled)
        return ((logged - self.means) / self.stds).astype(np.float32)

    def to_dict(self) -> dict[str, object]:
        return {
            "numeric_features": COMMON_NUMERIC_FEATURES,
            "medians": self.medians.tolist(),
            "means": self.means.tolist(),
            "stds": self.stds.tolist(),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train enhanced PCAP fusion model on the 5-class benchmark.")
    parser.add_argument(
        "--packet-data",
        default="data/paper_benchmark/encryption_method_5class_pcap_v1/packet/flows_5class.npz",
        help="Packet NPZ from build_paper_benchmark_dataset.py.",
    )
    parser.add_argument(
        "--hybrid-csv",
        default="data/paper_benchmark/encryption_method_5class_pcap_v1/hybrid/multiclass_finetune.csv",
        help="Hybrid/tabular CSV aligned with the packet NPZ row order.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/encryption_method/paper_methods_5class_v1/current_pcap_fusion",
        help="Output directory.",
    )
    parser.add_argument("--n-estimators", type=int, default=800, help="ExtraTrees estimator count.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--include-valid-in-train",
        action="store_true",
        help="Retrain on train+valid after method selection. Default keeps the shared train split only.",
    )
    return parser.parse_args()


def byte_histograms(packet_tensor: np.ndarray) -> np.ndarray:
    rows: list[np.ndarray] = []
    for sample in packet_tensor.astype(np.uint8, copy=False):
        counts = np.bincount(sample.reshape(-1), minlength=256).astype(np.float32)
        rows.append(counts / max(float(counts.sum()), 1.0))
    return np.stack(rows).astype(np.float32, copy=False)


def build_features(
    packet_tensor: np.ndarray,
    first_packets: np.ndarray,
    numeric_frame: pd.DataFrame,
    preprocessor: FusionPreprocessor,
) -> np.ndarray:
    numeric = preprocessor.transform_numeric(numeric_frame)
    hist = byte_histograms(packet_tensor)
    first = first_packets.astype(np.float32, copy=False) / 255.0
    return np.concatenate([numeric, hist, first], axis=1).astype(np.float32, copy=False)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    packet_bundle = np.load(Path(args.packet_data), allow_pickle=False)
    packet_tensor = packet_bundle["x"]
    first_packets = packet_bundle["x_first"]
    y = packet_bundle["y"].astype(np.int64)
    split = packet_bundle["split"].astype(str)
    label_names = packet_bundle["labels"].astype(str).tolist()

    numeric_frame = pd.read_csv(args.hybrid_csv, low_memory=False)
    if len(numeric_frame) != len(y):
        raise ValueError(
            "Hybrid CSV row count does not match packet NPZ row count: "
            f"{len(numeric_frame)} vs {len(y)}"
        )

    train_mask = split == "train"
    if args.include_valid_in_train:
        train_mask = train_mask | (split == "valid")
    test_mask = split == "test"
    train_indices = np.where(train_mask)[0]
    test_indices = np.where(test_mask)[0]

    preprocessor = FusionPreprocessor.fit(numeric_frame.iloc[train_indices])
    x_all = build_features(packet_tensor, first_packets, numeric_frame, preprocessor)

    model = ExtraTreesClassifier(
        n_estimators=args.n_estimators,
        random_state=args.random_state,
        class_weight="balanced",
        max_features="sqrt",
        min_samples_leaf=1,
        n_jobs=-1,
    )
    model.fit(x_all[train_indices], y[train_indices])
    y_pred = model.predict(x_all[test_indices])
    y_test = y[test_indices]

    metrics = compute_metrics(y_test, y_pred, label_names=label_names)
    metrics.update(
        {
            "model_name": "current_pcap_fusion",
            "method_description": "single-stage flow-statistics + byte-histogram + first-packet fusion",
            "packet_data": str(Path(args.packet_data)),
            "hybrid_csv": str(Path(args.hybrid_csv)),
            "samples_train": int(len(train_indices)),
            "samples_test": int(len(test_indices)),
            "num_features": int(x_all.shape[1]),
            "n_estimators": int(args.n_estimators),
            "include_valid_in_train": bool(args.include_valid_in_train),
            "random_state": int(args.random_state),
        }
    )

    write_metrics_bundle(output_dir, dict(metrics), label_names=label_names)
    np.savez_compressed(output_dir / "predictions.npz", y_true=y_test, y_pred=y_pred, test_indices=test_indices)
    joblib.dump(model, output_dir / "model.joblib")
    (output_dir / "feature_metadata.json").write_text(
        json.dumps(
            {
                **preprocessor.to_dict(),
                "feature_blocks": {
                    "numeric": len(COMMON_NUMERIC_FEATURES),
                    "byte_histogram": 256,
                    "first_packet_bytes": int(first_packets.shape[1]),
                },
                "feature_dim": int(x_all.shape[1]),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("Enhanced PCAP fusion training finished.")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"Macro-F1   : {metrics['f1_macro']:.4f}")
    print(f"Weighted-F1: {metrics['f1_weighted']:.4f}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
