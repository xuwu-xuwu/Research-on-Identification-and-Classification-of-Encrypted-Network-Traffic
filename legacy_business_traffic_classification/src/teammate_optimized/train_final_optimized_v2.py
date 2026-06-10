#!/usr/bin/env python
"""Optimized encrypted traffic classifier v2 with richer features and ensemble analysis."""

from __future__ import annotations

import argparse
import json
import re
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")


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


def safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / (denominator.abs() + 1.0)


def add_ratio_feature(df: pd.DataFrame, left: str, right: str, output: str) -> None:
    if left in df.columns and right in df.columns:
        df[output] = safe_div(df[left], df[right])


def add_log_feature(df: pd.DataFrame, source: str, output: str) -> None:
    if source in df.columns:
        clipped = df[source].clip(lower=0)
        df[output] = np.log1p(clipped)


def advanced_feature_engineering(df: pd.DataFrame, label_col: str) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    feature_df = df.copy()
    feature_cols = [col for col in feature_df.columns if col != label_col]

    for col in feature_cols:
        feature_df[col] = pd.to_numeric(feature_df[col], errors="coerce")
    feature_df = feature_df.replace([np.inf, -np.inf], np.nan)

    negative_missing_cols: list[str] = []
    for col in feature_cols:
        series = feature_df[col]
        if pd.api.types.is_numeric_dtype(series) and (series < 0).any():
            feature_df[f"{col}_is_missing"] = (series < 0).astype(int)
            feature_df.loc[series < 0, col] = np.nan
            negative_missing_cols.append(col)

    for col in feature_cols:
        if col in feature_df.columns and feature_df[col].isna().any() and f"{col}_nan_flag" not in feature_df.columns:
            feature_df[f"{col}_nan_flag"] = feature_df[col].isna().astype(int)

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

    numeric_cols = [col for col in feature_df.columns if col != label_col]
    quantile_capped_cols: list[str] = []
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(feature_df[col]):
            continue
        median = feature_df[col].median()
        if pd.isna(median):
            median = 0.0
        feature_df[col] = feature_df[col].fillna(median)

        q999 = feature_df[col].quantile(0.999)
        if pd.notna(q999) and (feature_df[col] > q999).any():
            feature_df.loc[feature_df[col] > q999, col] = q999
            quantile_capped_cols.append(col)

    constant_cols = [col for col in numeric_cols if feature_df[col].nunique(dropna=False) <= 1]
    if constant_cols:
        feature_df = feature_df.drop(columns=constant_cols)

    correlation_dropped_cols: list[str] = []
    corr_cols = [col for col in feature_df.columns if col != label_col]
    if corr_cols:
        corr_matrix = feature_df[corr_cols].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        for col in upper.columns:
            if any(upper[col] > 0.995):
                correlation_dropped_cols.append(col)
        if correlation_dropped_cols:
            feature_df = feature_df.drop(columns=correlation_dropped_cols)

    metadata = {
        "negative_missing_cols": sorted(negative_missing_cols),
        "quantile_capped_cols": sorted(set(quantile_capped_cols)),
        "constant_cols": sorted(constant_cols),
        "correlation_dropped_cols": sorted(correlation_dropped_cols),
        "final_feature_cols": [col for col in feature_df.columns if col != label_col],
    }
    return feature_df, metadata


def generate_weight_combos(num_models: int, step: float) -> list[tuple[float, ...]]:
    scaled_step = int(round(step * 100))
    if scaled_step <= 0 or 100 % scaled_step != 0:
        raise ValueError("weight step must divide 1.0 exactly, e.g. 0.1 or 0.2")

    total_units = int(round(1.0 / step))
    combos: list[tuple[float, ...]] = []

    def backtrack(index: int, remaining: int, current: list[int]) -> None:
        if index == num_models - 1:
            current.append(remaining)
            combos.append(tuple(round(value / total_units, 10) for value in current))
            current.pop()
            return
        for value in range(remaining + 1):
            current.append(value)
            backtrack(index + 1, remaining - value, current)
            current.pop()

    backtrack(0, total_units, [])
    return [combo for combo in combos if any(weight > 0 for weight in combo)]


def summarize_feature_importance(models: dict[str, object], feature_cols: list[str], output_path: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for model_name, model in models.items():
        importance = getattr(model, "feature_importances_", None)
        if importance is None:
            continue
        frame = pd.DataFrame(
            {
                "feature": feature_cols,
                f"importance_{model_name}": importance,
            }
        )
        frames.append(frame)

    if not frames:
        result = pd.DataFrame(columns=["feature"])
        result.to_csv(output_path, index=False)
        return result

    merged = frames[0]
    for frame in frames[1:]:
        merged = merged.merge(frame, on="feature", how="outer")
    merged = merged.fillna(0.0)

    importance_cols = [col for col in merged.columns if col.startswith("importance_")]
    merged["importance_mean"] = merged[importance_cols].mean(axis=1)
    merged = merged.sort_values("importance_mean", ascending=False)
    merged.to_csv(output_path, index=False)
    return merged


def build_error_analysis(
    x_test: pd.DataFrame,
    y_test: np.ndarray,
    y_pred: np.ndarray,
    pred_prob: np.ndarray,
    class_names: list[str],
    output_dir: Path,
) -> None:
    true_labels = [class_names[idx] for idx in y_test]
    pred_labels = [class_names[idx] for idx in y_pred]
    top1_conf = pred_prob.max(axis=1)
    sorted_prob = np.sort(pred_prob, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2]

    result_df = x_test.reset_index(drop=True).copy()
    result_df["y_true"] = true_labels
    result_df["y_pred"] = pred_labels
    result_df["confidence"] = top1_conf
    result_df["margin_top1_top2"] = margin
    result_df["is_correct"] = result_df["y_true"] == result_df["y_pred"]
    result_df.to_csv(output_dir / "test_predictions_detailed.csv", index=False)

    errors = result_df.loc[~result_df["is_correct"]].copy()
    errors = errors.sort_values(["confidence", "margin_top1_top2"], ascending=[True, True])
    errors.to_csv(output_dir / "misclassified_samples.csv", index=False)

    confusion_pairs = (
        errors.groupby(["y_true", "y_pred"]).size().reset_index(name="count").sort_values("count", ascending=False)
    )
    confusion_pairs.to_csv(output_dir / "misclassification_pairs.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train optimized encrypted traffic ensemble model v2.")
    parser.add_argument("--data", required=True, help="Path to ARFF or CSV dataset")
    parser.add_argument("--output", default="outputs/optimized/final_optimized_v2", help="Output directory")
    parser.add_argument("--label", default="class1", help="Label column name")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split ratio")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed")
    parser.add_argument("--weight-step", type=float, default=0.1, help="Ensemble search step, e.g. 0.1")
    parser.add_argument("--n-jobs", type=int, default=1, help="Parallel jobs for tree models")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Optimized encrypted traffic classifier v2")
    print("=" * 70)

    print("\n[1/6] Loading dataset...")
    df = load_dataset(data_path)
    if args.label not in df.columns:
        raise ValueError(f"Label column '{args.label}' not found.")
    print(f"Raw shape: {df.shape}")

    y = df[args.label].astype(str).str.strip()
    valid_mask = (~y.isna()) & (y != "") & (y != "?")
    df = df.loc[valid_mask].copy()
    df[args.label] = y.loc[valid_mask]

    print("\n[2/6] Feature engineering...")
    df, feature_meta = advanced_feature_engineering(df, args.label)
    feature_cols = [col for col in df.columns if col != args.label]
    print(f"Final feature count: {len(feature_cols)}")
    print(f"Dropped constant cols: {len(feature_meta['constant_cols'])}")
    print(f"Dropped high-corr cols: {len(feature_meta['correlation_dropped_cols'])}")

    le = LabelEncoder()
    y_encoded = le.fit_transform(df[args.label].astype(str))
    class_names = le.classes_.tolist()
    x = df[feature_cols].copy()

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y_encoded,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y_encoded,
    )
    print(f"Train samples: {len(x_train)}")
    print(f"Test samples : {len(x_test)}")
    print(f"Classes      : {class_names}")

    print("\n[3/6] Training base models...")
    chat_idx = class_names.index("CHAT") if "CHAT" in class_names else None
    streaming_idx = class_names.index("STREAMING") if "STREAMING" in class_names else None
    ft_idx = class_names.index("FT") if "FT" in class_names else None

    sample_weights = np.ones(len(y_train), dtype=float)
    if chat_idx is not None:
        sample_weights[y_train == chat_idx] = 2.0
    if streaming_idx is not None:
        sample_weights[y_train == streaming_idx] = 1.5
    if ft_idx is not None:
        sample_weights[y_train == ft_idx] = 1.3

    models: dict[str, object] = {}
    predictions: list[np.ndarray] = []

    xgb_weighted = xgb.XGBClassifier(
        n_estimators=650,
        max_depth=9,
        learning_rate=0.03,
        subsample=0.85,
        colsample_bytree=0.85,
        min_child_weight=3,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=args.random_state,
        n_jobs=args.n_jobs,
    )
    xgb_weighted.fit(x_train, y_train, sample_weight=sample_weights)
    models["xgb_weighted"] = xgb_weighted
    predictions.append(xgb_weighted.predict_proba(x_test))

    xgb_regular = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=8,
        learning_rate=0.035,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=args.random_state + 1,
        n_jobs=args.n_jobs,
    )
    xgb_regular.fit(x_train, y_train)
    models["xgb_regular"] = xgb_regular
    predictions.append(xgb_regular.predict_proba(x_test))

    rf_model = RandomForestClassifier(
        n_estimators=600,
        max_depth=22,
        min_samples_split=4,
        min_samples_leaf=1,
        class_weight="balanced_subsample",
        random_state=args.random_state + 2,
        n_jobs=args.n_jobs,
    )
    rf_model.fit(x_train, y_train)
    models["rf"] = rf_model
    predictions.append(rf_model.predict_proba(x_test))

    et_model = ExtraTreesClassifier(
        n_estimators=600,
        max_depth=None,
        min_samples_split=3,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=args.random_state + 3,
        n_jobs=args.n_jobs,
    )
    et_model.fit(x_train, y_train)
    models["extra_trees"] = et_model
    predictions.append(et_model.predict_proba(x_test))

    print(f"Trained models: {list(models.keys())}")

    print("\n[4/6] Searching ensemble weights...")
    weight_combos = generate_weight_combos(num_models=len(predictions), step=args.weight_step)
    print(f"Weight combinations: {len(weight_combos)}")

    best_macro_f1 = -1.0
    best_accuracy = -1.0
    best_weights: tuple[float, ...] | None = None
    best_prob: np.ndarray | None = None
    best_pred: np.ndarray | None = None

    for weights in weight_combos:
        ensemble_prob = np.zeros_like(predictions[0])
        for weight, pred_prob in zip(weights, predictions):
            ensemble_prob += weight * pred_prob

        y_pred = np.argmax(ensemble_prob, axis=1)
        macro_f1 = f1_score(y_test, y_pred, average="macro")
        accuracy = accuracy_score(y_test, y_pred)

        if macro_f1 > best_macro_f1 or (np.isclose(macro_f1, best_macro_f1) and accuracy > best_accuracy):
            best_macro_f1 = macro_f1
            best_accuracy = accuracy
            best_weights = weights
            best_prob = ensemble_prob
            best_pred = y_pred

    if best_weights is None or best_prob is None or best_pred is None:
        raise RuntimeError("Failed to find valid ensemble weights.")

    print(f"Best weights  : {best_weights}")
    print(f"Best accuracy : {best_accuracy:.4f}")
    print(f"Best macro F1 : {best_macro_f1:.4f}")

    print("\n[5/6] Writing reports...")
    report_text = classification_report(y_test, best_pred, target_names=class_names, digits=4)
    report_dict = classification_report(y_test, best_pred, target_names=class_names, digits=4, output_dict=True)
    recalls = recall_score(y_test, best_pred, average=None)
    cm = confusion_matrix(y_test, best_pred)

    print(report_text)

    metrics = {
        "data_path": str(data_path),
        "label_column": args.label,
        "samples_total": int(len(df)),
        "samples_train": int(len(x_train)),
        "samples_test": int(len(x_test)),
        "num_features": int(len(feature_cols)),
        "num_classes": int(len(class_names)),
        "accuracy": float(best_accuracy),
        "f1_macro": float(best_macro_f1),
        "best_weights": list(best_weights),
        "models": list(models.keys()),
        "feature_metadata": feature_meta,
        "class_recalls": {name: float(recall) for name, recall in zip(class_names, recalls)},
    }

    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(report_dict).transpose().to_csv(output_dir / "classification_report.csv", index=True)
    pd.DataFrame(cm, index=class_names, columns=class_names).to_csv(output_dir / "confusion_matrix.csv")

    summarize_feature_importance(models, feature_cols, output_dir / "feature_importance_summary.csv")
    build_error_analysis(x_test, y_test, best_pred, best_prob, class_names, output_dir)

    print("\n[6/6] Saving model bundle...")
    bundle = {
        "models": models,
        "weights": best_weights,
        "label_encoder": le,
        "feature_cols": feature_cols,
        "metrics": metrics,
        "feature_metadata": feature_meta,
    }
    joblib.dump(bundle, output_dir / "final_optimized_model.joblib")

    print(f"Output directory: {output_dir}")
    print("Saved files:")
    print("- classification_report.txt")
    print("- classification_report.csv")
    print("- confusion_matrix.csv")
    print("- metrics.json")
    print("- feature_importance_summary.csv")
    print("- test_predictions_detailed.csv")
    print("- misclassified_samples.csv")
    print("- misclassification_pairs.csv")
    print("- final_optimized_model.joblib")


if __name__ == "__main__":
    main()
