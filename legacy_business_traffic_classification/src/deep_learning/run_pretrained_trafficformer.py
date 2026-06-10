#!/usr/bin/env python
"""Run the reproduced TrafficFormer fine-tuning pipeline as a standalone deep-learning branch."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def parse_metrics(log_text: str) -> dict[str, object]:
    metrics: dict[str, object] = {}

    acc_matches = re.findall(r"Acc\. \(Correct/Total\):\s*([0-9.]+)\s*\((\d+)/(\d+)\)", log_text)
    if acc_matches:
        acc_match = acc_matches[-1]
        metrics["accuracy"] = float(acc_match[0])
        metrics["correct"] = int(acc_match[1])
        metrics["total"] = int(acc_match[2])

    macro_precision_matches = re.findall(r"Macro precision:\s*([0-9.]+)", log_text)
    macro_recall_matches = re.findall(r"Macro recall:\s*([0-9.]+)", log_text)
    macro_f1_matches = re.findall(r"Macro f1:\s*([0-9.]+)", log_text)
    weighted_f1_matches = re.findall(r"Weighted f1:\s*([0-9.]+)", log_text)

    if macro_precision_matches:
        metrics["macro_precision"] = float(macro_precision_matches[-1])
    if macro_recall_matches:
        metrics["macro_recall"] = float(macro_recall_matches[-1])
    if macro_f1_matches:
        metrics["macro_f1"] = float(macro_f1_matches[-1])
    if weighted_f1_matches:
        metrics["weighted_f1"] = float(weighted_f1_matches[-1])

    label_rows = []
    for match in re.finditer(r"Label\s+(\d+):\s*([0-9.]+),\s*([0-9.]+),\s*([0-9.]+)", log_text):
        label_rows.append(
            {
                "label_id": int(match.group(1)),
                "precision": float(match.group(2)),
                "recall": float(match.group(3)),
                "f1": float(match.group(4)),
            }
        )
    if label_rows:
        metrics["per_label"] = label_rows

    if not metrics:
        raise ValueError("Failed to parse metrics from TrafficFormer log output.")
    return metrics


def build_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TrafficFormer fine-tuning as an independent transformer branch.")
    parser.add_argument("--trafficformer-root", required=True, help="Path to the TrafficFormer reproduction root.")
    parser.add_argument("--train-path", required=True, help="Training TSV path, relative to TrafficFormer root or absolute.")
    parser.add_argument("--dev-path", required=True, help="Validation TSV path, relative to TrafficFormer root or absolute.")
    parser.add_argument("--test-path", required=True, help="Test TSV path, relative to TrafficFormer root or absolute.")
    parser.add_argument("--output-dir", required=True, help="Directory for logs, metrics, and output model.")
    parser.add_argument("--run-name", default="trafficformer_run", help="User-facing run name.")
    parser.add_argument("--epochs", type=int, default=10, help="Maximum epochs.")
    parser.add_argument("--earlystop", type=int, default=4, help="Early stopping rounds.")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size.")
    parser.add_argument("--seq-length", type=int, default=320, help="Sequence length.")
    parser.add_argument("--learning-rate", type=float, default=6e-5, help="Learning rate.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed passed to TrafficFormer.")
    return parser.parse_args()


def main() -> None:
    args = build_args()
    trafficformer_root = Path(args.trafficformer_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not trafficformer_root.exists():
        raise FileNotFoundError(f"TrafficFormer root not found: {trafficformer_root}")

    model_output_path = output_dir / "model.bin"
    command = [
        sys.executable,
        "fine-tuning/run_classifier.py",
        "--vocab_path",
        "models/encryptd_vocab.txt",
        "--train_path",
        args.train_path,
        "--dev_path",
        args.dev_path,
        "--test_path",
        args.test_path,
        "--pretrained_model_path",
        "models/pretrain_model.bin",
        "--output_model_path",
        str(model_output_path),
        "--epochs_num",
        str(args.epochs),
        "--earlystop",
        str(args.earlystop),
        "--batch_size",
        str(args.batch_size),
        "--embedding",
        "word_pos_seg",
        "--encoder",
        "transformer",
        "--mask",
        "fully_visible",
        "--seq_length",
        str(args.seq_length),
        "--learning_rate",
        str(args.learning_rate),
        "--seed",
        str(args.seed),
        "--config_path",
        "models/bert/base_config.json",
    ]

    process = subprocess.run(
        command,
        cwd=str(trafficformer_root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    combined_log = process.stdout + "\n" + process.stderr
    (output_dir / "train.log").write_text(combined_log, encoding="utf-8")

    if process.returncode != 0:
        raise RuntimeError(
            "TrafficFormer fine-tuning failed. "
            f"See log: {output_dir / 'train.log'}"
        )

    metrics = parse_metrics(process.stdout)
    metrics["run_name"] = args.run_name
    metrics["return_code"] = process.returncode
    metrics["train_path"] = args.train_path
    metrics["dev_path"] = args.dev_path
    metrics["test_path"] = args.test_path
    metrics["epochs"] = args.epochs
    metrics["earlystop"] = args.earlystop
    metrics["batch_size"] = args.batch_size
    metrics["seq_length"] = args.seq_length
    metrics["learning_rate"] = args.learning_rate
    metrics["seed"] = args.seed
    metrics["model_output_path"] = str(model_output_path)
    metrics["trafficformer_root"] = str(trafficformer_root)

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "command.json").write_text(json.dumps(command, indent=2, ensure_ascii=False), encoding="utf-8")

    print("TrafficFormer transformer run finished.")
    print(f"Run name   : {args.run_name}")
    if "accuracy" in metrics:
        print(f"Accuracy   : {metrics['accuracy']:.4f}")
    if "macro_f1" in metrics:
        print(f"Macro F1   : {metrics['macro_f1']:.4f}")
    if "weighted_f1" in metrics:
        print(f"Weighted F1: {metrics['weighted_f1']:.4f}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
