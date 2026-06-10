#!/usr/bin/env python
"""Train fair full-data tabular baselines for encryption-method identification.

This benchmark intentionally excludes `source_name` to avoid dataset-origin
leakage in the main comparison table.
"""

from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier

from unified_benchmark_utils import (
    UnifiedTabularPreprocessor,
    compute_metrics,
    encode_labels,
    load_multiclass_splits,
    write_metrics_bundle,
)

warnings.filterwarnings("ignore")


SUPPORTED_MODELS = ("rf", "extra_trees", "xgboost")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark full-data tabular baselines on unified encryption-method data.")
    parser.add_argument(
        "--data-dir",
        default="data/unified_encryption_method_v2_all_data",
        help="Directory containing multiclass_finetune.csv and metadata.json.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/encryption_method/tabular_main_table_v1",
        help="Directory for baseline benchmark outputs.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=list(SUPPORTED_MODELS),
        choices=SUPPORTED_MODELS,
        help="Baseline models to train.",
    )
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--use-transport", action="store_true", help="Append one-hot transport features.")
    parser.add_argument("--rf-estimators", type=int, default=300, help="RandomForest tree count.")
    parser.add_argument("--extra-trees-estimators", type=int, default=400, help="ExtraTrees tree count.")
    parser.add_argument("--xgb-estimators", type=int, default=600, help="XGBoost tree count.")
    parser.add_argument("--xgb-max-depth", type=int, default=8, help="XGBoost tree depth.")
    parser.add_argument("--xgb-learning-rate", type=float, default=0.05, help="XGBoost learning rate.")
    return parser.parse_args()


def build_model(name: str, args: argparse.Namespace, num_classes: int) -> object:
    if name == "rf":
        return RandomForestClassifier(
            n_estimators=args.rf_estimators,
            random_state=args.random_state,
            n_jobs=-1,
            class_weight="balanced_subsample",
            min_samples_leaf=2,
        )
    if name == "extra_trees":
        return ExtraTreesClassifier(
            n_estimators=args.extra_trees_estimators,
            random_state=args.random_state,
            n_jobs=-1,
            class_weight="balanced_subsample",
            min_samples_leaf=2,
        )
    if name == "xgboost":
        return xgb.XGBClassifier(
            objective="multi:softprob",
            num_class=num_classes,
            n_estimators=args.xgb_estimators,
            max_depth=args.xgb_max_depth,
            learning_rate=args.xgb_learning_rate,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=2,
            reg_alpha=0.0,
            reg_lambda=1.0,
            random_state=args.random_state,
            n_jobs=-1,
            tree_method="hist",
            eval_metric="mlogloss",
        )
    raise ValueError(f"Unsupported model: {name}")


def train_and_evaluate(
    model_name: str,
    model: object,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_valid: np.ndarray,
    y_valid: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    label_names: list[str],
) -> dict[str, object]:
    if model_name == "xgboost":
        model.fit(
            x_train,
            y_train,
            eval_set=[(x_valid, y_valid)],
            verbose=False,
        )
    else:
        model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    metrics = compute_metrics(y_test, y_pred, label_names=label_names)
    metrics["model_name"] = model_name
    metrics["samples_train"] = int(len(x_train))
    metrics["samples_valid"] = int(len(x_valid))
    metrics["samples_test"] = int(len(x_test))
    metrics["num_features"] = int(x_train.shape[1])
    return metrics


def main() -> None:
    args = parse_args()
    splits = load_multiclass_splits(args.data_dir)

    preprocessor = UnifiedTabularPreprocessor(include_transport=args.use_transport).fit(splits.train)
    x_train = preprocessor.transform(splits.train)
    x_valid = preprocessor.transform(splits.valid)
    x_test = preprocessor.transform(splits.test)

    y_train = encode_labels(splits.train["final_label"], splits.label_names)
    y_valid = encode_labels(splits.valid["final_label"], splits.label_names)
    y_test = encode_labels(splits.test["final_label"], splits.label_names)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "feature_metadata.json").write_text(
        json.dumps(preprocessor.metadata(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    comparison_rows: list[dict[str, object]] = []

    for model_name in args.models:
        model = build_model(model_name, args=args, num_classes=len(splits.label_names))
        metrics = train_and_evaluate(
            model_name=model_name,
            model=model,
            x_train=x_train,
            y_train=y_train,
            x_valid=x_valid,
            y_valid=y_valid,
            x_test=x_test,
            y_test=y_test,
            label_names=splits.label_names,
        )

        model_output_dir = output_dir / model_name
        model_output_dir.mkdir(parents=True, exist_ok=True)
        write_metrics_bundle(model_output_dir, dict(metrics), label_names=splits.label_names)
        joblib.dump(model, model_output_dir / "model.joblib")

        comparison_rows.append(
            {
                "model_name": model_name,
                "accuracy": metrics["accuracy"],
                "f1_macro": metrics["f1_macro"],
                "f1_weighted": metrics["f1_weighted"],
                "macro_recall": metrics["macro_recall"],
                "num_features": metrics["num_features"],
            }
        )

    comparison_df = pd.DataFrame(comparison_rows).sort_values(
        by=["f1_macro", "accuracy"],
        ascending=[False, False],
    )
    comparison_df.to_csv(output_dir / "comparison.csv", index=False)
    (output_dir / "comparison.json").write_text(
        json.dumps(comparison_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    markdown_lines = [
        "# Fair Full-Data Tabular Baselines",
        "",
        f"- Data dir: `{Path(args.data_dir)}`",
        f"- Source leakage guard: `source_name` excluded",
        f"- Transport one-hot enabled: `{args.use_transport}`",
        "",
        comparison_df.to_markdown(index=False),
        "",
    ]
    (output_dir / "comparison.md").write_text("\n".join(markdown_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
