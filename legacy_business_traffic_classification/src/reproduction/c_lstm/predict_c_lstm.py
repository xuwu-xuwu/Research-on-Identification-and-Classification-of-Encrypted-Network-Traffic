#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from common import (
    extract_paper_bytes,
    iter_capture_entries,
    iter_packets,
    materialize_capture,
    pad_or_truncate,
)
from train_c_lstm import CLSTMClassifier, resolve_device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run inference with a trained C-LSTM model.")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--data", help="Prepared .npz packet dataset.")
    mode_group.add_argument(
        "--sources",
        nargs="+",
        help="Directories or zip archives containing raw PCAP/PCAPNG files.",
    )

    parser.add_argument("--model", required=True, help="Path to model.pt checkpoint.")
    parser.add_argument("--output-dir", required=True, help="Directory for inference outputs.")
    parser.add_argument("--batch-size", type=int, default=128, help="Inference batch size.")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda.")
    parser.add_argument(
        "--splits",
        default=None,
        help="Optional splits.npz path when predicting on a prepared dataset.",
    )
    parser.add_argument(
        "--split-key",
        default="test_indices",
        help="Key inside splits.npz to select prediction indices.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional limit for prepared-dataset prediction rows.",
    )
    parser.add_argument(
        "--max-packets-per-file",
        type=int,
        default=0,
        help="Limit packets read from each capture in raw-source mode. 0 keeps all.",
    )
    parser.add_argument(
        "--include-labels",
        nargs="*",
        default=None,
        help="Optional label filter in raw-source mode.",
    )
    return parser.parse_args()


def load_model(checkpoint_path: Path, device: torch.device) -> tuple[CLSTMClassifier, list[str], int]:
    checkpoint = torch.load(checkpoint_path, map_location=device)
    labels = checkpoint["labels"]
    packet_size = int(checkpoint["packet_size"])
    model = CLSTMClassifier(num_classes=len(labels)).to(device)
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, labels, packet_size


def predict_probabilities(
    model: CLSTMClassifier,
    x: np.ndarray,
    batch_size: int,
    device: torch.device,
) -> np.ndarray:
    probabilities: list[np.ndarray] = []
    with torch.no_grad():
        for start in range(0, len(x), batch_size):
            batch = torch.from_numpy(x[start : start + batch_size]).to(device)
            logits = model(batch)
            batch_probs = torch.softmax(logits, dim=1).cpu().numpy()
            probabilities.append(batch_probs)
    return np.concatenate(probabilities, axis=0)


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
            "mean_confidence": float(group["confidence"].mean()),
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

    y_true = records["true_label"].tolist()
    y_pred = records["predicted_label"].tolist()
    accuracy = float((records["true_label"] == records["predicted_label"]).mean())

    per_label = {}
    for label in labels:
        label_mask = records["true_label"] == label
        support = int(label_mask.sum())
        if support == 0:
            continue
        recall = float((records.loc[label_mask, "predicted_label"] == label).mean())
        per_label[label] = {
            "support": support,
            "recall": recall,
        }

    return {
        "num_predictions": int(len(records)),
        "accuracy": accuracy,
        "per_label_recall": per_label,
    }


def prepare_rows_from_npz(args: argparse.Namespace) -> tuple[np.ndarray, pd.DataFrame]:
    bundle = np.load(Path(args.data), allow_pickle=False)
    x = bundle["x"]
    row_indices = np.arange(len(x))
    if args.splits:
        split_bundle = np.load(Path(args.splits), allow_pickle=False)
        if args.split_key not in split_bundle:
            raise KeyError(f"Split key '{args.split_key}' not found in {args.splits}")
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


def prepare_rows_from_raw_sources(
    args: argparse.Namespace,
    packet_size: int,
) -> tuple[np.ndarray, pd.DataFrame]:
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
                packet_rows.append(pad_or_truncate(retained, packet_size=packet_size))
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

    return np.stack(packet_rows).astype(np.uint8, copy=False), pd.DataFrame(metadata_rows)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    device = resolve_device(args.device)
    model, labels, packet_size = load_model(Path(args.model), device)

    if args.data:
        x, records = prepare_rows_from_npz(args)
        input_mode = "prepared_dataset"
    else:
        x, records = prepare_rows_from_raw_sources(args, packet_size=packet_size)
        input_mode = "raw_captures"

    probabilities = predict_probabilities(model, x=x, batch_size=args.batch_size, device=device)
    predicted_indices = probabilities.argmax(axis=1)
    confidences = probabilities.max(axis=1)

    records = records.copy()
    records["predicted_index"] = predicted_indices.astype(int)
    records["predicted_label"] = [labels[index] for index in predicted_indices]
    records["confidence"] = confidences.astype(float)

    summary = {
        "model_path": str(Path(args.model)),
        "input_mode": input_mode,
        "num_predictions": int(len(records)),
        "num_classes": int(len(labels)),
        "labels": labels,
        "device": str(device),
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
