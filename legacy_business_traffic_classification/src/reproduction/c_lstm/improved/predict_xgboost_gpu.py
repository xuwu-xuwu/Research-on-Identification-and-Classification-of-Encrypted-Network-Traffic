#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from xgboost import XGBClassifier

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import extract_paper_bytes, iter_capture_entries, iter_packets, materialize_capture, pad_or_truncate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run inference with a trained GPU XGBoost packet classifier.")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--data", help="Prepared .npz packet dataset.")
    mode_group.add_argument("--sources", nargs="+", help="Directories or zip archives containing raw captures.")

    parser.add_argument("--model", required=True, help="Path to XGBoost model.json.")
    parser.add_argument("--model-meta", required=True, help="Path to model_meta.json.")
    parser.add_argument("--output-dir", required=True, help="Directory for inference outputs.")
    parser.add_argument("--device", default="cpu", help="XGBoost device for inference, e.g. cpu or cuda.")
    parser.add_argument("--splits", default=None, help="Optional splits.npz path for prepared dataset mode.")
    parser.add_argument("--split-key", default="test_indices", help="Split key inside splits.npz.")
    parser.add_argument("--limit", type=int, default=0, help="Optional row limit in prepared dataset mode.")
    parser.add_argument("--max-packets-per-file", type=int, default=0, help="Limit packets per capture in raw mode.")
    parser.add_argument("--include-labels", nargs="*", default=None, help="Optional raw-capture label filter.")
    return parser.parse_args()


def load_model(model_path: Path, model_meta_path: Path, device: str) -> tuple[XGBClassifier, list[str], int]:
    meta = json.loads(model_meta_path.read_text(encoding="utf-8"))
    model = XGBClassifier()
    model.load_model(model_path)
    model.set_params(device=device)
    return model, meta["labels"], int(meta["packet_size"])


def build_capture_summary(records: pd.DataFrame) -> list[dict[str, object]]:
    grouped_rows: list[dict[str, object]] = []
    for capture_name, group in records.groupby("capture_name", sort=True):
        predicted_counts = Counter(group["predicted_label"].tolist())
        top_label, top_count = predicted_counts.most_common(1)[0]
        item: dict[str, object] = {
            "capture_name": capture_name,
            "num_packets": int(len(group)),
            "top_predicted_label": top_label,
            "top_predicted_ratio": float(top_count / len(group)),
            "predicted_label_counts": dict(predicted_counts),
        }
        if "true_label" in group.columns and group["true_label"].notna().all():
            true_labels = group["true_label"].unique().tolist()
            if len(true_labels) == 1:
                item["true_label"] = true_labels[0]
                item["capture_level_correct"] = bool(true_labels[0] == top_label)
        grouped_rows.append(item)
    return grouped_rows


def build_metrics(records: pd.DataFrame, labels: list[str]) -> dict[str, object] | None:
    if "true_label" not in records.columns or records["true_label"].isna().any():
        return None

    accuracy = float((records["true_label"] == records["predicted_label"]).mean())
    per_label = {}
    for label in labels:
        label_mask = records["true_label"] == label
        support = int(label_mask.sum())
        if support == 0:
            continue
        recall = float((records.loc[label_mask, "predicted_label"] == label).mean())
        per_label[label] = {"support": support, "recall": recall}

    return {
        "num_predictions": int(len(records)),
        "accuracy": accuracy,
        "per_label_recall": per_label,
    }


def prepare_rows_from_npz(args: argparse.Namespace) -> tuple[np.ndarray, pd.DataFrame]:
    bundle = np.load(Path(args.data), allow_pickle=False)
    x = bundle["x"].astype(np.float32, copy=False)
    row_indices = np.arange(len(x))
    if args.splits:
        split_bundle = np.load(Path(args.splits), allow_pickle=False)
        row_indices = split_bundle[args.split_key]
    if args.limit > 0:
        row_indices = row_indices[: args.limit]

    records = pd.DataFrame({"row_index": row_indices.astype(int)})
    if "y" in bundle and "labels" in bundle:
        label_names = bundle["labels"].tolist()
        y = bundle["y"][row_indices]
        records["true_label"] = [label_names[index] for index in y]
    if "source_index" in bundle and "sources" in bundle:
        sources = bundle["sources"].tolist()
        source_index = bundle["source_index"][row_indices]
        records["capture_name"] = [sources[index] for index in source_index]
    else:
        records["capture_name"] = "prepared_dataset"
    return x[row_indices], records


def prepare_rows_from_raw_sources(args: argparse.Namespace, packet_size: int) -> tuple[np.ndarray, pd.DataFrame]:
    include_labels = set(args.include_labels) if args.include_labels else None
    entries = list(iter_capture_entries([Path(source) for source in args.sources], include_labels=include_labels))
    if not entries:
        raise ValueError("No capture files matched the provided raw sources.")

    packet_rows: list[np.ndarray] = []
    metadata_rows: list[dict[str, object]] = []
    for entry in entries:
        packet_counter = 0
        with materialize_capture(entry) as capture_path:
            for packet in iter_packets(capture_path):
                retained = extract_paper_bytes(packet)
                if retained is None:
                    continue
                packet_rows.append(pad_or_truncate(retained, packet_size=packet_size).astype(np.float32, copy=False))
                metadata_rows.append(
                    {
                        "capture_name": entry.display_name,
                        "true_label": entry.label,
                        "packet_index_in_capture": packet_counter,
                    }
                )
                packet_counter += 1
                if args.max_packets_per_file > 0 and packet_counter >= args.max_packets_per_file:
                    break

    if not packet_rows:
        raise ValueError("No packets were retained from the provided raw captures.")
    return np.stack(packet_rows), pd.DataFrame(metadata_rows)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model, labels, packet_size = load_model(Path(args.model), Path(args.model_meta), args.device)

    if args.data:
        x, records = prepare_rows_from_npz(args)
        input_mode = "prepared_dataset"
    else:
        x, records = prepare_rows_from_raw_sources(args, packet_size)
        input_mode = "raw_captures"

    predicted_indices = np.asarray(model.predict(x)).reshape(-1).astype(int)
    predicted_labels = [labels[index] for index in predicted_indices]

    records = records.copy()
    records["predicted_index"] = predicted_indices
    records["predicted_label"] = predicted_labels

    summary = {
        "model_path": str(Path(args.model)),
        "input_mode": input_mode,
        "num_predictions": int(len(records)),
        "num_classes": int(len(labels)),
        "labels": labels,
        "device": args.device,
    }
    metrics = build_metrics(records, labels)
    if metrics is not None:
        summary["metrics"] = metrics

    capture_summary = build_capture_summary(records)
    records.to_csv(output_dir / "packet_predictions.csv", index=False, encoding="utf-8")
    (output_dir / "capture_predictions.json").write_text(
        json.dumps(capture_summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (output_dir / "prediction_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Prediction finished.")
    print(f"Input mode  : {input_mode}")
    print(f"Predictions : {len(records)}")
    if metrics is not None:
        print(f"Accuracy    : {metrics['accuracy']:.4f}")
    print(f"Output dir  : {output_dir}")


if __name__ == "__main__":
    main()
