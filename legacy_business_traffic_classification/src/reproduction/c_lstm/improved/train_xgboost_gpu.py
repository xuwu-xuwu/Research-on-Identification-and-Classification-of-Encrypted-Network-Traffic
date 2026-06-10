#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier

sys.path.append(str(Path(__file__).resolve().parents[1]))
from train_c_lstm import save_confusion_matrix


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a GPU XGBoost packet classifier.")
    parser.add_argument("--data", required=True, help="Path to prepared packet dataset (.npz).")
    parser.add_argument("--output-dir", required=True, help="Directory for outputs.")
    parser.add_argument("--splits", default=None, help="Optional splits.npz path to reuse train/test split.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split ratio when splits are not provided.")
    parser.add_argument(
        "--split-mode",
        choices=("random", "capture"),
        default="random",
        help="Split packets randomly or by capture/source group.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--n-estimators", type=int, default=300, help="Number of boosting rounds.")
    parser.add_argument("--max-depth", type=int, default=10, help="Maximum tree depth.")
    parser.add_argument("--learning-rate", type=float, default=0.08, help="Learning rate.")
    parser.add_argument("--subsample", type=float, default=0.9, help="Row subsampling ratio.")
    parser.add_argument("--colsample-bytree", type=float, default=0.9, help="Feature subsampling ratio.")
    parser.add_argument("--min-child-weight", type=float, default=1.0, help="Minimum child weight.")
    parser.add_argument("--gamma", type=float, default=0.0, help="Minimum loss reduction for further partition.")
    parser.add_argument("--reg-alpha", type=float, default=0.0, help="L1 regularization.")
    parser.add_argument("--reg-lambda", type=float, default=1.0, help="L2 regularization.")
    parser.add_argument("--max-bin", type=int, default=256, help="Maximum histogram bins.")
    parser.add_argument("--device", default="cuda", help="XGBoost device, e.g. cuda or cpu.")
    parser.add_argument(
        "--class-weight",
        choices=("none", "balanced"),
        default="none",
        help="Optional class reweighting applied on the training partition.",
    )
    parser.add_argument("--n-jobs", type=int, default=8, help="CPU threads used by XGBoost.")
    return parser.parse_args()


def build_capture_split(
    labels: np.ndarray,
    source_index: np.ndarray,
    test_size: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    unique_sources = np.unique(source_index)
    label_to_sources: dict[int, list[int]] = {}

    for group_id in unique_sources:
        group_mask = source_index == group_id
        group_labels = np.unique(labels[group_mask])
        if group_labels.size != 1:
            raise ValueError(f"Capture group {group_id} contains multiple labels, cannot build group split.")
        group_label = int(group_labels[0])
        label_to_sources.setdefault(group_label, []).append(int(group_id))

    test_groups: list[int] = []
    for group_label, group_ids in sorted(label_to_sources.items()):
        shuffled_groups = np.asarray(group_ids, dtype=np.int64)
        rng.shuffle(shuffled_groups)
        if shuffled_groups.size < 2:
            raise ValueError(
                f"Label index {group_label} only has {shuffled_groups.size} capture, cannot create capture split."
            )

        requested = int(np.round(shuffled_groups.size * test_size))
        n_test_groups = min(max(requested, 1), shuffled_groups.size - 1)
        test_groups.extend(shuffled_groups[:n_test_groups].tolist())

    test_group_set = set(test_groups)
    all_indices = np.arange(labels.shape[0], dtype=np.int64)
    test_mask = np.isin(source_index, np.asarray(sorted(test_group_set), dtype=np.int64))
    test_indices = all_indices[test_mask]
    train_indices = all_indices[~test_mask]

    if train_indices.size == 0 or test_indices.size == 0:
        raise ValueError("Capture split produced an empty train or test partition.")

    return train_indices, test_indices


def main() -> None:
    args = parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Prepared dataset not found: {data_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle = np.load(data_path, allow_pickle=False)
    x = bundle["x"].astype(np.float32, copy=False)
    y = bundle["y"]
    labels = bundle["labels"].tolist()
    source_index = bundle["source_index"] if "source_index" in bundle.files else None
    sources = bundle["sources"].tolist() if "sources" in bundle.files else None

    if args.splits:
        split_bundle = np.load(Path(args.splits), allow_pickle=False)
        train_indices = split_bundle["train_indices"]
        test_indices = split_bundle["test_indices"]
        split_mode = str(split_bundle["split_mode"].tolist()) if "split_mode" in split_bundle.files else "reused"
    else:
        split_mode = args.split_mode
        if args.split_mode == "capture":
            if source_index is None:
                raise ValueError("Dataset does not contain source_index; capture split is unavailable.")
            train_indices, test_indices = build_capture_split(
                labels=y,
                source_index=source_index,
                test_size=args.test_size,
                seed=args.seed,
            )
        else:
            all_indices = np.arange(len(y))
            train_indices, test_indices = train_test_split(
                all_indices,
                test_size=args.test_size,
                random_state=args.seed,
                stratify=y,
            )

    x_train = x[train_indices]
    x_test = x[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]

    model = XGBClassifier(
        objective="multi:softprob",
        num_class=len(labels),
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        subsample=args.subsample,
        colsample_bytree=args.colsample_bytree,
        min_child_weight=args.min_child_weight,
        gamma=args.gamma,
        reg_alpha=args.reg_alpha,
        reg_lambda=args.reg_lambda,
        max_bin=args.max_bin,
        eval_metric="mlogloss",
        tree_method="hist",
        device=args.device,
        random_state=args.seed,
        n_jobs=args.n_jobs,
        verbosity=1,
    )
    fit_kwargs = {}
    if args.class_weight == "balanced":
        fit_kwargs["sample_weight"] = compute_sample_weight(class_weight="balanced", y=y_train)
    model.fit(x_train, y_train, **fit_kwargs)

    if args.device.startswith("cuda"):
        model.get_booster().set_param({"device": "cpu"})

    y_pred = np.asarray(model.predict(x_test)).reshape(-1).astype(int)

    metrics = {
        "data_path": str(data_path),
        "samples_total": int(len(y)),
        "samples_train": int(len(train_indices)),
        "samples_test": int(len(test_indices)),
        "num_classes": int(len(labels)),
        "packet_size": int(x.shape[1]),
        "seed": int(args.seed),
        "device": args.device,
        "class_weight": args.class_weight,
        "split_mode": split_mode,
        "n_estimators": int(args.n_estimators),
        "max_depth": int(args.max_depth),
        "learning_rate": float(args.learning_rate),
        "subsample": float(args.subsample),
        "colsample_bytree": float(args.colsample_bytree),
        "min_child_weight": float(args.min_child_weight),
        "gamma": float(args.gamma),
        "reg_alpha": float(args.reg_alpha),
        "reg_lambda": float(args.reg_lambda),
        "max_bin": int(args.max_bin),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_test, y_pred, average="weighted")),
    }

    report_text = classification_report(
        y_test,
        y_pred,
        target_names=labels,
        digits=4,
        zero_division=0,
    )
    report_dict = classification_report(
        y_test,
        y_pred,
        target_names=labels,
        digits=4,
        zero_division=0,
        output_dict=True,
    )
    cm = confusion_matrix(y_test, y_pred, labels=np.arange(len(labels)))

    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (output_dir / "classification_report.txt").write_text(report_text, encoding="utf-8")
    (output_dir / "classification_report.json").write_text(json.dumps(report_dict, indent=2), encoding="utf-8")
    save_confusion_matrix(cm, labels, output_dir / "confusion_matrix.png")
    split_payload: dict[str, np.ndarray] = {
        "train_indices": train_indices,
        "test_indices": test_indices,
        "split_mode": np.asarray(split_mode),
    }
    if source_index is not None:
        split_payload["train_groups"] = np.unique(source_index[train_indices])
        split_payload["test_groups"] = np.unique(source_index[test_indices])
    np.savez_compressed(output_dir / "splits.npz", **split_payload)
    np.savez_compressed(output_dir / "predictions.npz", y_true=y_test, y_pred=y_pred, indices=test_indices)
    model.get_booster().save_model(output_dir / "model.json")
    (output_dir / "model_meta.json").write_text(
        json.dumps(
            {
                "labels": labels,
                "packet_size": int(x.shape[1]),
                "data_path": str(data_path),
                "model_type": "xgboost_gpu_packet_classifier",
                "split_mode": split_mode,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    if source_index is not None and sources is not None:
        train_group_ids = np.unique(source_index[train_indices]).astype(int)
        test_group_ids = np.unique(source_index[test_indices]).astype(int)
        split_summary = {
            "split_mode": split_mode,
            "train_captures": [sources[group_id] for group_id in train_group_ids.tolist()],
            "test_captures": [sources[group_id] for group_id in test_group_ids.tolist()],
            "num_train_captures": int(train_group_ids.size),
            "num_test_captures": int(test_group_ids.size),
        }
        (output_dir / "split_summary.json").write_text(json.dumps(split_summary, indent=2), encoding="utf-8")

    print("XGBoost GPU training finished.")
    print(f"Accuracy   : {metrics['accuracy']:.4f}")
    print(f"F1 (macro) : {metrics['f1_macro']:.4f}")
    print(f"F1 (weight): {metrics['f1_weighted']:.4f}")
    print(f"Output dir : {output_dir}")


if __name__ == "__main__":
    main()
