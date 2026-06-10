#!/usr/bin/env python
from __future__ import annotations

import argparse
import importlib
import json
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np

from common import (
    PAPER_LABEL_ORDER,
    extract_paper_bytes,
    iter_capture_entries,
    iter_packets,
    materialize_capture,
    ordered_labels,
    pad_or_truncate,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare a paper-style C-LSTM packet dataset from PCAP/PCAPNG sources."
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        required=True,
        help="Directories or zip archives containing PCAP/PCAPNG files.",
    )
    parser.add_argument("--output", required=True, help="Output .npz dataset path.")
    parser.add_argument("--packet-size", type=int, default=1480, help="Packet vector length.")
    parser.add_argument(
        "--min-bytes",
        type=int,
        default=1,
        help="Minimum retained bytes after preprocessing.",
    )
    parser.add_argument(
        "--max-packets-per-file",
        type=int,
        default=0,
        help="Limit packets extracted from each capture. 0 keeps all.",
    )
    parser.add_argument(
        "--max-packets-per-class",
        type=int,
        default=0,
        help="Limit packets extracted for each class. 0 keeps all.",
    )
    parser.add_argument(
        "--include-labels",
        nargs="*",
        default=None,
        help="Optional explicit label filter. Defaults to every known paper label found.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = [Path(source) for source in args.sources]
    for source in sources:
        if not source.exists():
            raise FileNotFoundError(f"Capture source not found: {source}")

    include_labels = set(args.include_labels) if args.include_labels else None
    entries = list(iter_capture_entries(sources, include_labels=include_labels))
    if not entries:
        raise ValueError("No labeled capture files were found in the provided sources.")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    packet_rows: list[np.ndarray] = []
    label_rows: list[str] = []
    source_index_rows: list[int] = []
    capture_names = [entry.display_name for entry in entries]

    packets_per_class: Counter[str] = Counter()
    packets_per_capture: dict[str, int] = {}
    skipped_packets = 0

    for source_index, entry in enumerate(entries):
        if args.max_packets_per_class > 0 and packets_per_class[entry.label] >= args.max_packets_per_class:
            packets_per_capture[entry.display_name] = 0
            continue

        extracted_for_capture = 0
        with materialize_capture(entry) as capture_path:
            for packet in iter_packets(capture_path):
                retained = extract_paper_bytes(packet)
                if retained is None or len(retained) < args.min_bytes:
                    skipped_packets += 1
                    continue

                if args.max_packets_per_class > 0 and packets_per_class[entry.label] >= args.max_packets_per_class:
                    break
                if args.max_packets_per_file > 0 and extracted_for_capture >= args.max_packets_per_file:
                    break

                packet_rows.append(pad_or_truncate(retained, packet_size=args.packet_size))
                label_rows.append(entry.label)
                source_index_rows.append(source_index)
                packets_per_class[entry.label] += 1
                extracted_for_capture += 1

        packets_per_capture[entry.display_name] = extracted_for_capture

    if not packet_rows:
        raise ValueError("No packets were retained after preprocessing.")

    label_names = ordered_labels(label_rows)
    label_to_index = {label: index for index, label in enumerate(label_names)}

    x = np.stack(packet_rows).astype(np.uint8, copy=False)
    y = np.asarray([label_to_index[label] for label in label_rows], dtype=np.int64)
    source_index = np.asarray(source_index_rows, dtype=np.int64)

    # zipfile-inflate64 patches zipfile for reading Deflate64 archives and breaks NumPy zip writes.
    importlib.reload(zipfile)
    np.savez_compressed(
        output_path,
        x=x,
        y=y,
        labels=np.asarray(label_names, dtype="<U32"),
        source_index=source_index,
        sources=np.asarray(capture_names, dtype="<U256"),
    )

    missing_paper_labels = [label for label in PAPER_LABEL_ORDER if label not in packets_per_class]
    summary = {
        "output_path": str(output_path),
        "num_packets": int(x.shape[0]),
        "packet_size": int(args.packet_size),
        "num_classes": int(len(label_names)),
        "classes": label_names,
        "packets_per_class": dict(sorted(packets_per_class.items())),
        "packets_per_capture": packets_per_capture,
        "skipped_packets": int(skipped_packets),
        "sources": [str(source) for source in sources],
        "missing_paper_labels_in_local_data": missing_paper_labels,
    }

    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Dataset preparation finished.")
    print(f"Output dataset : {output_path}")
    print(f"Summary        : {summary_path}")
    print(f"Packets        : {summary['num_packets']}")
    print(f"Classes        : {summary['classes']}")
    if missing_paper_labels:
        print(f"Missing labels : {missing_paper_labels}")


if __name__ == "__main__":
    main()

