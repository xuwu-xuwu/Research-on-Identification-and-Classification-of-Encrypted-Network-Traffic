#!/usr/bin/env python
"""Train a broad fallback model for incomplete encryption-method inputs.

The main full model should still be used when all 21 flow-level numeric
features are available. This fallback model is trained with synthetic missing
feature scenarios, so it can be used when a request only provides partial flow
features, transport, and optional sequence_text.
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

from src.encryption_method.train_full_enhanced_fusion import (  # noqa: E402
    SEQUENCE_FEATURE_NAMES,
    encode_transport,
    extract_sequence_features,
    sample_weights,
)
from src.encryption_method.unified_benchmark_utils import (  # noqa: E402
    COMMON_NUMERIC_FEATURES,
    compute_metrics,
    encode_labels,
    safe_log1p,
)


@dataclass
class BroadFallbackPreprocessor:
    numeric_medians: np.ndarray
    numeric_means: np.ndarray
    numeric_stds: np.ndarray
    sequence_means: np.ndarray
    sequence_stds: np.ndarray
    transport_categories: list[str]

    @classmethod
    def fit(cls, frame: pd.DataFrame) -> "BroadFallbackPreprocessor":
        numeric_raw = frame[COMMON_NUMERIC_FEATURES].to_numpy(dtype=np.float32, copy=True)
        medians = np.nanmedian(numeric_raw, axis=0)
        medians = np.where(np.isnan(medians), 0.0, medians)
        filled = np.where(np.isnan(numeric_raw), medians, numeric_raw)
        logged = safe_log1p(filled)
        numeric_means = logged.mean(axis=0)
        numeric_stds = logged.std(axis=0)
        numeric_stds = np.where(numeric_stds < 1e-6, 1.0, numeric_stds)

        sequence_raw = extract_sequence_features(frame["sequence_text"].fillna("").astype(str).to_numpy())
        sequence_raw[:, 1:] = safe_log1p(sequence_raw[:, 1:])
        sequence_means = sequence_raw.mean(axis=0)
        sequence_stds = sequence_raw.std(axis=0)
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
        missing_mask = np.isnan(numeric_raw).astype(np.float32)
        filled = np.where(np.isnan(numeric_raw), self.numeric_medians, numeric_raw)
        logged = safe_log1p(filled)
        numeric = ((logged - self.numeric_means) / self.numeric_stds).astype(np.float32)
        numeric = np.where(missing_mask > 0.0, 0.0, numeric).astype(np.float32)

        transport = encode_transport(
            frame["transport"].fillna("OTHER").astype(str).str.upper().to_numpy(),
            self.transport_categories,
        )

        sequence = extract_sequence_features(frame["sequence_text"].fillna("").astype(str).to_numpy())
        sequence[:, 1:] = safe_log1p(sequence[:, 1:])
        sequence = ((sequence - self.sequence_means) / self.sequence_stds).astype(np.float32)

        return np.concatenate([numeric, missing_mask, transport, sequence], axis=1).astype(np.float32, copy=False)

    def to_dict(self) -> dict[str, object]:
        return {
            "preprocessor_type": "broad_fallback",
            "numeric_features": COMMON_NUMERIC_FEATURES,
            "numeric_medians": self.numeric_medians.tolist(),
            "numeric_means": self.numeric_means.tolist(),
            "numeric_stds": self.numeric_stds.tolist(),
            "transport_categories": self.transport_categories,
            "sequence_features": SEQUENCE_FEATURE_NAMES,
            "sequence_means": self.sequence_means.tolist(),
            "sequence_stds": self.sequence_stds.tolist(),
            "feature_blocks": {
                "numeric_values": len(COMMON_NUMERIC_FEATURES),
                "numeric_missing_indicators": len(COMMON_NUMERIC_FEATURES),
                "transport": len(self.transport_categories),
                "sequence_derived": len(SEQUENCE_FEATURE_NAMES),
            },
            "feature_dim": len(COMMON_NUMERIC_FEATURES) * 2 + len(self.transport_categories) + len(SEQUENCE_FEATURE_NAMES),
            "source_name_excluded": True,
            "routing_role": "fallback_when_numeric_features_incomplete",
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train broad fallback model for incomplete encryption-method inputs.")
    parser.add_argument("--data-dir", default="data/unified_encryption_method_v2_all_data")
    parser.add_argument("--output-dir", default="outputs/encryption_method/broad_fallback_v1")
    parser.add_argument("--n-estimators", type=int, default=220)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--learning-rate", type=float, default=0.06)
    parser.add_argument("--subsample", type=float, default=0.88)
    parser.add_argument("--colsample-bytree", type=float, default=0.88)
    parser.add_argument("--min-child-weight", type=float, default=2.0)
    parser.add_argument("--class-weight-power", type=float, default=0.5)
    parser.add_argument("--partial-missing-prob", type=float, default=0.6)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--n-jobs", type=int, default=-1)
    return parser.parse_args()


def scenario_frame(frame: pd.DataFrame, scenario: str, rng: np.random.Generator, partial_prob: float) -> pd.DataFrame:
    result = frame.copy()
    result.loc[:, COMMON_NUMERIC_FEATURES] = result[COMMON_NUMERIC_FEATURES].astype(np.float32)
    if scenario == "full":
        return result
    if scenario == "no_numeric":
        result.loc[:, COMMON_NUMERIC_FEATURES] = np.nan
        return result
    if scenario == "transport_only":
        result.loc[:, COMMON_NUMERIC_FEATURES] = np.nan
        result.loc[:, "sequence_text"] = ""
        return result
    if scenario == "partial_numeric":
        numeric = result[COMMON_NUMERIC_FEATURES].to_numpy(dtype=np.float32, copy=True)
        mask = rng.random(numeric.shape) < partial_prob
        numeric[mask] = np.nan
        result.loc[:, COMMON_NUMERIC_FEATURES] = numeric
        return result
    raise ValueError(f"Unknown scenario: {scenario}")


def build_augmented_train(
    train_frame: pd.DataFrame,
    preprocessor: BroadFallbackPreprocessor,
    y_train: np.ndarray,
    rng: np.random.Generator,
    partial_prob: float,
) -> tuple[np.ndarray, np.ndarray]:
    frames = [
        scenario_frame(train_frame, "full", rng, partial_prob),
        scenario_frame(train_frame, "partial_numeric", rng, partial_prob),
        scenario_frame(train_frame, "no_numeric", rng, partial_prob),
        scenario_frame(train_frame, "transport_only", rng, partial_prob),
    ]
    x_parts = [preprocessor.transform(frame) for frame in frames]
    y_parts = [y_train for _ in frames]
    return np.vstack(x_parts).astype(np.float32), np.concatenate(y_parts).astype(np.int64)


def scenario_metrics(
    model: xgb.XGBClassifier,
    preprocessor: BroadFallbackPreprocessor,
    test_frame: pd.DataFrame,
    y_test: np.ndarray,
    label_names: list[str],
    rng: np.random.Generator,
    partial_prob: float,
) -> dict[str, dict[str, object]]:
    scenarios: dict[str, dict[str, object]] = {}
    for scenario in ["full", "partial_numeric", "no_numeric", "transport_only"]:
        frame = scenario_frame(test_frame, scenario, rng, partial_prob)
        predictions = model.predict(preprocessor.transform(frame))
        metrics = compute_metrics(y_test, predictions, label_names)
        metrics.pop("classification_report_text", None)
        scenarios[scenario] = metrics
    return scenarios


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.random_state)
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = json.loads((data_dir / "metadata.json").read_text(encoding="utf-8"))
    label_names = list(metadata["final_label_order"])
    usecols = ["split", "final_label", "transport", "sequence_text"] + COMMON_NUMERIC_FEATURES
    frame = pd.read_csv(data_dir / "multiclass_finetune.csv", usecols=usecols, low_memory=False)

    train_frame = frame.loc[frame["split"] == "train"].copy()
    test_frame = frame.loc[frame["split"] == "test"].copy()
    if train_frame.empty or test_frame.empty:
        raise ValueError("Dataset must contain non-empty train and test splits.")

    preprocessor = BroadFallbackPreprocessor.fit(train_frame)
    y_train = encode_labels(train_frame["final_label"], label_names)
    y_test = encode_labels(test_frame["final_label"], label_names)
    x_train, y_train_augmented = build_augmented_train(
        train_frame=train_frame,
        preprocessor=preprocessor,
        y_train=y_train,
        rng=rng,
        partial_prob=args.partial_missing_prob,
    )
    weights = sample_weights(y_train_augmented, num_classes=len(label_names), power=args.class_weight_power)

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
    model.fit(x_train, y_train_augmented, sample_weight=weights, verbose=False)

    scenarios = scenario_metrics(
        model=model,
        preprocessor=preprocessor,
        test_frame=test_frame,
        y_test=y_test,
        label_names=label_names,
        rng=np.random.default_rng(args.random_state + 1000),
        partial_prob=args.partial_missing_prob,
    )
    primary = scenarios["no_numeric"]
    metrics = {
        "model_name": "broad_fallback_xgboost",
        "method_description": "missing-robust fallback model for incomplete flow-feature inputs",
        "routing_role": "fallback_when_21_numeric_features_are_incomplete",
        "data_dir": str(data_dir),
        "samples_train_base": int(len(train_frame)),
        "samples_train_augmented": int(len(y_train_augmented)),
        "samples_test": int(len(test_frame)),
        "num_features": int(x_train.shape[1]),
        "partial_missing_prob": float(args.partial_missing_prob),
        "source_name_excluded": True,
        "accuracy": primary["accuracy"],
        "f1_macro": primary["f1_macro"],
        "f1_weighted": primary["f1_weighted"],
        "macro_recall": primary["macro_recall"],
        "primary_eval_scenario": "no_numeric",
        "evaluation_scenarios": scenarios,
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

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    model.save_model(output_dir / "model.json")
    joblib.dump(model, output_dir / "model.joblib")
    (output_dir / "feature_metadata.json").write_text(
        json.dumps(preprocessor.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary = pd.DataFrame(
        [
            {
                "scenario": scenario,
                "accuracy": values["accuracy"],
                "f1_macro": values["f1_macro"],
                "f1_weighted": values["f1_weighted"],
                "macro_recall": values["macro_recall"],
            }
            for scenario, values in scenarios.items()
        ]
    )
    summary.to_csv(output_dir / "comparison.csv", index=False)
    markdown = [
        "# Broad Fallback Model",
        "",
        "- Routing role: used when the 21 numeric flow features are incomplete.",
        "- Training augmentation: full + partial numeric missing + all numeric missing + transport-only.",
        f"- Base train samples: `{len(train_frame)}`",
        f"- Augmented train samples: `{len(y_train_augmented)}`",
        "",
        summary.to_markdown(index=False),
        "",
    ]
    (output_dir / "comparison.md").write_text("\n".join(markdown), encoding="utf-8")

    print("Broad fallback training finished.")
    print(summary.to_string(index=False))
    print(f"Output dir: {output_dir}")


if __name__ == "__main__":
    main()
