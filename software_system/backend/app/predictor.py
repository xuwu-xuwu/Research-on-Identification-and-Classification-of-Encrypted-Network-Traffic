from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd


def safe_log1p(values: np.ndarray) -> np.ndarray:
    return np.sign(values) * np.log1p(np.abs(values))


def parse_bucket_suffix(token: str) -> float | None:
    try:
        return float(token.rsplit("_", 1)[1])
    except (IndexError, ValueError):
        return None


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


def extract_sequence_features(texts: np.ndarray) -> np.ndarray:
    features = np.zeros((len(texts), len(SEQUENCE_FEATURE_NAMES)), dtype=np.float32)
    for row_index, text in enumerate(texts):
        if not str(text).strip():
            continue

        fwd_lengths: list[float] = []
        bwd_lengths: list[float] = []
        iats: list[float] = []
        tokens = str(text).split()
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


@dataclass(frozen=True)
class PredictorMetadata:
    model_name: str
    label_names: list[str]
    numeric_features: list[str]
    transport_categories: list[str]
    sequence_features: list[str]
    metrics: dict[str, Any]
    routing: dict[str, Any] | None = None


class ModelPredictor:
    def __init__(self, model_dir: str | Path, data_metadata_path: str | Path | None = None) -> None:
        self.model_dir = Path(model_dir)
        self.data_metadata_path = Path(data_metadata_path) if data_metadata_path else None
        self.model = None
        self.feature_metadata: dict[str, Any] = {}
        self.metrics: dict[str, Any] = {}
        self.label_names: list[str] = []
        self.model_name = "unknown"

    def load(self) -> "ModelPredictor":
        model_path = self.model_dir / "model.joblib"
        feature_metadata_path = self.model_dir / "feature_metadata.json"
        metrics_path = self.model_dir / "metrics.json"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not feature_metadata_path.exists():
            raise FileNotFoundError(f"Feature metadata not found: {feature_metadata_path}")
        if not metrics_path.exists():
            raise FileNotFoundError(f"Metrics file not found: {metrics_path}")

        self.model = joblib.load(model_path)
        self.feature_metadata = json.loads(feature_metadata_path.read_text(encoding="utf-8"))
        self.metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        self.model_name = str(self.metrics.get("model_name", self.model_dir.name))
        self.label_names = self._load_label_names()
        return self

    @property
    def loaded(self) -> bool:
        return self.model is not None

    def metadata(self) -> PredictorMetadata:
        return PredictorMetadata(
            model_name=self.model_name,
            label_names=self.label_names,
            numeric_features=list(self.feature_metadata["numeric_features"]),
            transport_categories=list(self.feature_metadata.get("transport_categories", [])),
            sequence_features=list(self.feature_metadata.get("sequence_features", [])),
            metrics=self.metrics,
        )

    def _load_label_names(self) -> list[str]:
        if self.data_metadata_path and self.data_metadata_path.exists():
            data_metadata = json.loads(self.data_metadata_path.read_text(encoding="utf-8"))
            labels = list(data_metadata.get("final_label_order", []))
            if labels:
                return labels
        class_recalls = self.metrics.get("class_recalls", {})
        if isinstance(class_recalls, dict) and class_recalls:
            return list(class_recalls.keys())
        raise ValueError("Unable to infer label order from data metadata or metrics.")

    def frame_from_records(self, records: list[dict[str, Any]]) -> pd.DataFrame:
        if not records:
            raise ValueError("At least one record is required.")
        frame = pd.DataFrame(records)
        for column in self.feature_metadata["numeric_features"]:
            if column not in frame.columns:
                frame[column] = np.nan
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        if "transport" not in frame.columns:
            frame["transport"] = "OTHER"
        if "sequence_text" not in frame.columns:
            frame["sequence_text"] = ""
        return frame

    def transform(self, frame: pd.DataFrame) -> np.ndarray:
        if self.feature_metadata.get("preprocessor_type") == "broad_fallback":
            return self._transform_broad_fallback(frame)
        return self._transform_full_fusion(frame)

    def _transform_full_fusion(self, frame: pd.DataFrame) -> np.ndarray:
        numeric_features = list(self.feature_metadata["numeric_features"])
        numeric_raw = frame[numeric_features].to_numpy(dtype=np.float32, copy=True)
        medians = np.asarray(self.feature_metadata["numeric_medians"], dtype=np.float32)
        means = np.asarray(self.feature_metadata["numeric_means"], dtype=np.float32)
        stds = np.asarray(self.feature_metadata["numeric_stds"], dtype=np.float32)
        numeric_filled = np.where(np.isnan(numeric_raw), medians, numeric_raw)
        numeric_logged = safe_log1p(numeric_filled)
        numeric = ((numeric_logged - means) / stds).astype(np.float32)

        transport_categories = list(self.feature_metadata.get("transport_categories", []))
        transport_values = frame["transport"].fillna("OTHER").astype(str).str.upper().to_numpy()
        transport = encode_transport(transport_values, transport_categories)

        sequence_raw = extract_sequence_features(frame["sequence_text"].fillna("").astype(str).to_numpy())
        sequence_raw[:, 1:] = safe_log1p(sequence_raw[:, 1:])
        sequence_means = np.asarray(self.feature_metadata["sequence_means"], dtype=np.float32)
        sequence_stds = np.asarray(self.feature_metadata["sequence_stds"], dtype=np.float32)
        sequence = ((sequence_raw - sequence_means) / sequence_stds).astype(np.float32)

        features = np.concatenate([numeric, transport, sequence], axis=1).astype(np.float32, copy=False)
        expected_dim = int(self.feature_metadata.get("feature_dim", features.shape[1]))
        if features.shape[1] != expected_dim:
            raise ValueError(f"Feature dimension mismatch: got {features.shape[1]}, expected {expected_dim}")
        return features

    def _transform_broad_fallback(self, frame: pd.DataFrame) -> np.ndarray:
        numeric_features = list(self.feature_metadata["numeric_features"])
        numeric_raw = frame[numeric_features].to_numpy(dtype=np.float32, copy=True)
        missing_mask = np.isnan(numeric_raw).astype(np.float32)
        medians = np.asarray(self.feature_metadata["numeric_medians"], dtype=np.float32)
        means = np.asarray(self.feature_metadata["numeric_means"], dtype=np.float32)
        stds = np.asarray(self.feature_metadata["numeric_stds"], dtype=np.float32)
        numeric_filled = np.where(np.isnan(numeric_raw), medians, numeric_raw)
        numeric_logged = safe_log1p(numeric_filled)
        numeric = ((numeric_logged - means) / stds).astype(np.float32)
        numeric = np.where(missing_mask > 0.0, 0.0, numeric).astype(np.float32)

        transport_categories = list(self.feature_metadata.get("transport_categories", []))
        transport_values = frame["transport"].fillna("OTHER").astype(str).str.upper().to_numpy()
        transport = encode_transport(transport_values, transport_categories)

        sequence_raw = extract_sequence_features(frame["sequence_text"].fillna("").astype(str).to_numpy())
        sequence_raw[:, 1:] = safe_log1p(sequence_raw[:, 1:])
        sequence_means = np.asarray(self.feature_metadata["sequence_means"], dtype=np.float32)
        sequence_stds = np.asarray(self.feature_metadata["sequence_stds"], dtype=np.float32)
        sequence = ((sequence_raw - sequence_means) / sequence_stds).astype(np.float32)

        features = np.concatenate([numeric, missing_mask, transport, sequence], axis=1).astype(np.float32, copy=False)
        expected_dim = int(self.feature_metadata.get("feature_dim", features.shape[1]))
        if features.shape[1] != expected_dim:
            raise ValueError(f"Feature dimension mismatch: got {features.shape[1]}, expected {expected_dim}")
        return features

    def predict_records(self, records: list[dict[str, Any]], include_probabilities: bool = False) -> list[dict[str, Any]]:
        frame = self.frame_from_records(records)
        return self.predict_frame(frame, include_probabilities=include_probabilities)

    def predict_frame(self, frame: pd.DataFrame, include_probabilities: bool = False) -> list[dict[str, Any]]:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        features = self.transform(frame)
        probabilities = self.model.predict_proba(features)
        predicted_ids = np.argmax(probabilities, axis=1)

        outputs: list[dict[str, Any]] = []
        for index, predicted_id in enumerate(predicted_ids):
            row_probabilities = probabilities[index]
            item: dict[str, Any] = {
                "index": int(index),
                "predicted_label": self.label_names[int(predicted_id)],
                "confidence": float(row_probabilities[int(predicted_id)]),
            }
            if include_probabilities:
                item["probabilities"] = {
                    label: float(row_probabilities[label_index])
                    for label_index, label in enumerate(self.label_names)
                }
            outputs.append(item)
        return outputs

    def predict_csv_text(self, csv_text: str, include_probabilities: bool = False) -> list[dict[str, Any]]:
        from io import StringIO

        frame = pd.read_csv(StringIO(csv_text), low_memory=False)
        predictions = self.predict_frame(self.frame_from_records(frame.to_dict(orient="records")), include_probabilities)
        original_rows = frame.fillna("").to_dict(orient="records")
        merged: list[dict[str, Any]] = []
        for row, prediction in zip(original_rows, predictions):
            result = dict(row)
            result["predicted_label"] = prediction["predicted_label"]
            result["confidence"] = prediction["confidence"]
            if include_probabilities:
                for label, probability in prediction.get("probabilities", {}).items():
                    result[f"prob_{label}"] = probability
            merged.append(result)
        return merged


def missing_numeric_features(record: dict[str, Any], numeric_features: list[str]) -> list[str]:
    missing: list[str] = []
    for feature in numeric_features:
        if feature not in record:
            missing.append(feature)
            continue
        value = record.get(feature)
        if value is None or value == "":
            missing.append(feature)
            continue
        try:
            if pd.isna(pd.to_numeric(value, errors="coerce")):
                missing.append(feature)
        except Exception:
            missing.append(feature)
    return missing


class RoutedModelPredictor:
    def __init__(
        self,
        primary_model_dir: str | Path,
        fallback_model_dir: str | Path,
        data_metadata_path: str | Path | None = None,
    ) -> None:
        self.primary = ModelPredictor(primary_model_dir, data_metadata_path=data_metadata_path)
        self.fallback = ModelPredictor(fallback_model_dir, data_metadata_path=data_metadata_path)
        self.fallback_available = False
        self.model_name = "routed_full_enhanced_plus_broad_fallback"
        self.label_names: list[str] = []

    def load(self) -> "RoutedModelPredictor":
        self.primary.load()
        try:
            self.fallback.load()
            self.fallback_available = True
        except FileNotFoundError:
            self.fallback_available = False
        self.label_names = self.primary.label_names
        return self

    @property
    def loaded(self) -> bool:
        return self.primary.loaded and (self.fallback.loaded if self.fallback_available else True)

    def metadata(self) -> PredictorMetadata:
        primary_metadata = self.primary.metadata()
        fallback_metrics = self.fallback.metrics if self.fallback_available else {}
        return PredictorMetadata(
            model_name=self.model_name,
            label_names=primary_metadata.label_names,
            numeric_features=primary_metadata.numeric_features,
            transport_categories=primary_metadata.transport_categories,
            sequence_features=primary_metadata.sequence_features,
            metrics=primary_metadata.metrics,
            routing={
                "primary_model": self.primary.model_name,
                "fallback_model": self.fallback.model_name if self.fallback_available else None,
                "fallback_available": self.fallback_available,
                "policy": "complete_21_numeric_features_use_primary_else_fallback",
                "fallback_primary_eval_scenario": fallback_metrics.get("primary_eval_scenario"),
                "fallback_metrics": {
                    "accuracy": fallback_metrics.get("accuracy"),
                    "f1_macro": fallback_metrics.get("f1_macro"),
                    "f1_weighted": fallback_metrics.get("f1_weighted"),
                    "macro_recall": fallback_metrics.get("macro_recall"),
                },
            },
        )

    def _select_model(self, record: dict[str, Any]) -> tuple[ModelPredictor, str, list[str]]:
        missing = missing_numeric_features(record, self.primary.feature_metadata["numeric_features"])
        if not missing:
            return self.primary, "complete_21_numeric", missing
        if self.fallback_available:
            return self.fallback, "incomplete_numeric_fallback", missing
        return self.primary, "incomplete_numeric_primary_imputation", missing

    def predict_records(self, records: list[dict[str, Any]], include_probabilities: bool = False) -> list[dict[str, Any]]:
        if not records:
            raise ValueError("At least one record is required.")
        outputs: list[dict[str, Any] | None] = [None] * len(records)
        grouped: dict[str, dict[str, Any]] = {}
        for index, record in enumerate(records):
            model, profile, missing = self._select_model(record)
            group = grouped.setdefault(
                model.model_name,
                {"model": model, "indices": [], "records": [], "profiles": [], "missing": []},
            )
            group["indices"].append(index)
            group["records"].append(record)
            group["profiles"].append(profile)
            group["missing"].append(missing)

        for group in grouped.values():
            model = group["model"]
            predictions = model.predict_records(group["records"], include_probabilities=include_probabilities)
            for local_index, prediction in enumerate(predictions):
                original_index = group["indices"][local_index]
                prediction["index"] = int(original_index)
                prediction["model_used"] = model.model_name
                prediction["input_profile"] = group["profiles"][local_index]
                prediction["missing_numeric_features"] = group["missing"][local_index]
                outputs[original_index] = prediction

        return [item for item in outputs if item is not None]

    def predict_csv_text(self, csv_text: str, include_probabilities: bool = False) -> list[dict[str, Any]]:
        from io import StringIO

        frame = pd.read_csv(StringIO(csv_text), low_memory=False)
        records = frame.to_dict(orient="records")
        predictions = self.predict_records(records, include_probabilities=include_probabilities)
        original_rows = frame.fillna("").to_dict(orient="records")
        merged: list[dict[str, Any]] = []
        for row, prediction in zip(original_rows, predictions):
            result = dict(row)
            result["predicted_label"] = prediction["predicted_label"]
            result["confidence"] = prediction["confidence"]
            result["model_used"] = prediction.get("model_used")
            result["input_profile"] = prediction.get("input_profile")
            result["missing_numeric_features"] = ";".join(prediction.get("missing_numeric_features", []))
            if include_probabilities:
                for label, probability in prediction.get("probabilities", {}).items():
                    result[f"prob_{label}"] = probability
            merged.append(result)
        return merged
