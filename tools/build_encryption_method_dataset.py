#!/usr/bin/env python
"""Build a first-pass encryption-method traffic dataset from local PCAP files.

The script uses tshark packet dissection to derive visible encryption protocol
labels such as TLS, QUIC/GQUIC, SSH, DTLS, OpenVPN, and WireGuard. It aggregates
packets into bidirectional 5-tuple flows and writes tabular features plus a
simple packet-length sequence representation under data/encryption_method_identification.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


CAPTURE_EXTENSIONS = {".pcap", ".pcapng"}
DEFAULT_OUTPUT_DIR = Path("data/encryption_method_identification")
UNKNOWN_LABEL = "UNKNOWN_OR_NON_ENCRYPTED"
LABEL_PRIORITY = [
    "WIREGUARD",
    "OPENVPN",
    "SSH",
    "QUIC",
    "DTLS",
    "TLS",
]


def normalize_protocol(raw_protocol: str) -> str:
    proto = raw_protocol.upper()
    if "WIREGUARD" in proto:
        return "WIREGUARD"
    if "OPENVPN" in proto:
        return "OPENVPN"
    if "SSH" in proto:
        return "SSH"
    if "GQUIC" in proto or "QUIC" in proto or "HTTP3" in proto:
        return "QUIC"
    if "DTLS" in proto:
        return "DTLS"
    if "TLS" in proto or "SSL" in proto:
        return "TLS"
    return ""


def first_value(value: str) -> str:
    if not value:
        return ""
    return value.split(",")[0].strip()


def to_float(value: str, default: float = 0.0) -> float:
    try:
        return float(first_value(value))
    except (TypeError, ValueError):
        return default


def to_int(value: str, default: int = 0) -> int:
    try:
        return int(float(first_value(value)))
    except (TypeError, ValueError):
        return default


def classify_source_group(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    if "vpn-pcaps-02" in parts:
        return "vpn_named_source"
    if "nonvpn-pcaps-01" in parts:
        return "nonvpn_named_source"
    if "nonvpn-pcaps-03" in parts:
        return "nonvpn_named_source"
    return "unknown_source"


def infer_business_hint(path: Path) -> str:
    name = path.stem.lower()
    rules = [
        ("file_transfer", ["scp", "sftp", "ftp", "files", "file"]),
        ("streaming", ["youtube", "netflix", "vimeo", "spotify", "video"]),
        ("voip", ["audio", "voipbuster", "voip"]),
        ("chat", ["chat", "aim", "icq"]),
        ("email", ["email", "mail"]),
    ]
    for label, patterns in rules:
        if any(pattern in name for pattern in patterns):
            return label
    return "unknown"


def canonical_flow_key(
    src: str,
    dst: str,
    sport: str,
    dport: str,
    transport: str,
) -> tuple[str, tuple[str, str], tuple[str, str]]:
    endpoint_a = (src, sport)
    endpoint_b = (dst, dport)
    if endpoint_b < endpoint_a:
        endpoint_a, endpoint_b = endpoint_b, endpoint_a
    return transport, endpoint_a, endpoint_b


def bucket_len(length: int) -> str:
    capped = min(max(length, 0), 2000)
    bucket = int(round(capped / 50.0) * 50)
    return f"{bucket:04d}"


def bucket_iat(seconds: float) -> str:
    milliseconds = min(max(seconds * 1000.0, 0.0), 10000.0)
    if milliseconds <= 10:
        bucket = int(round(milliseconds))
    elif milliseconds <= 100:
        bucket = int(round(milliseconds / 10.0) * 10)
    else:
        bucket = int(round(milliseconds / 100.0) * 100)
    return f"{bucket:05d}"


@dataclass
class FlowStats:
    capture_path: str
    capture_name: str
    source_group: str
    business_hint: str
    transport: str
    endpoint_a_ip: str
    endpoint_a_port: str
    endpoint_b_ip: str
    endpoint_b_port: str
    first_time: float
    last_time: float
    packet_count: int = 0
    byte_count: int = 0
    fwd_packet_count: int = 0
    fwd_byte_count: int = 0
    bwd_packet_count: int = 0
    bwd_byte_count: int = 0
    sum_len: float = 0.0
    sum_len_sq: float = 0.0
    min_len: int = field(default_factory=lambda: 2**31 - 1)
    max_len: int = 0
    iat_count: int = 0
    iat_sum: float = 0.0
    iat_sum_sq: float = 0.0
    iat_min: float = field(default_factory=lambda: math.inf)
    iat_max: float = 0.0
    last_seen_time: float | None = None
    protocol_counts: Counter[str] = field(default_factory=Counter)
    encryption_counts: Counter[str] = field(default_factory=Counter)
    sequence_tokens: list[str] = field(default_factory=list)

    def update(
        self,
        timestamp: float,
        length: int,
        protocol: str,
        encryption_label: str,
        src: str,
        sport: str,
        max_sequence_packets: int,
    ) -> None:
        self.packet_count += 1
        self.byte_count += length
        self.last_time = max(self.last_time, timestamp)
        self.sum_len += length
        self.sum_len_sq += length * length
        self.min_len = min(self.min_len, length)
        self.max_len = max(self.max_len, length)
        self.protocol_counts[protocol or "UNKNOWN"] += 1
        if encryption_label:
            self.encryption_counts[encryption_label] += 1

        is_forward = src == self.endpoint_a_ip and sport == self.endpoint_a_port
        if is_forward:
            self.fwd_packet_count += 1
            self.fwd_byte_count += length
            direction = "F"
        else:
            self.bwd_packet_count += 1
            self.bwd_byte_count += length
            direction = "B"

        if self.last_seen_time is not None:
            iat = max(timestamp - self.last_seen_time, 0.0)
            self.iat_count += 1
            self.iat_sum += iat
            self.iat_sum_sq += iat * iat
            self.iat_min = min(self.iat_min, iat)
            self.iat_max = max(self.iat_max, iat)
        else:
            iat = 0.0
        self.last_seen_time = timestamp

        if len(self.sequence_tokens) < max_sequence_packets * 2:
            self.sequence_tokens.append(f"{direction}_LEN_{bucket_len(length)}")
            self.sequence_tokens.append(f"IAT_{bucket_iat(iat)}")

    def label(self) -> tuple[str, float]:
        total_encrypted = sum(self.encryption_counts.values())
        if total_encrypted == 0:
            return UNKNOWN_LABEL, 0.0
        best_count = max(self.encryption_counts.values())
        candidates = [label for label, count in self.encryption_counts.items() if count == best_count]
        for label in LABEL_PRIORITY:
            if label in candidates:
                return label, best_count / total_encrypted
        return sorted(candidates)[0], best_count / total_encrypted

    def to_row(self, flow_id: int) -> dict[str, object]:
        label, label_confidence = self.label()
        duration = max(self.last_time - self.first_time, 0.0)
        mean_len = self.sum_len / self.packet_count if self.packet_count else 0.0
        len_var = max((self.sum_len_sq / self.packet_count) - mean_len * mean_len, 0.0) if self.packet_count else 0.0
        mean_iat = self.iat_sum / self.iat_count if self.iat_count else 0.0
        iat_var = max((self.iat_sum_sq / self.iat_count) - mean_iat * mean_iat, 0.0) if self.iat_count else 0.0
        encrypted_packets = sum(self.encryption_counts.values())

        return {
            "flow_id": flow_id,
            "encryption_method": label,
            "label_confidence": round(label_confidence, 6),
            "capture_name": self.capture_name,
            "capture_path": self.capture_path,
            "source_group": self.source_group,
            "business_hint": self.business_hint,
            "transport": self.transport,
            "endpoint_a_ip": self.endpoint_a_ip,
            "endpoint_a_port": self.endpoint_a_port,
            "endpoint_b_ip": self.endpoint_b_ip,
            "endpoint_b_port": self.endpoint_b_port,
            "packet_count": self.packet_count,
            "byte_count": self.byte_count,
            "duration": duration,
            "packets_per_second": self.packet_count / (duration + 1e-9),
            "bytes_per_second": self.byte_count / (duration + 1e-9),
            "fwd_packet_count": self.fwd_packet_count,
            "fwd_byte_count": self.fwd_byte_count,
            "bwd_packet_count": self.bwd_packet_count,
            "bwd_byte_count": self.bwd_byte_count,
            "direction_packet_ratio": self.fwd_packet_count / (self.bwd_packet_count + 1.0),
            "direction_byte_ratio": self.fwd_byte_count / (self.bwd_byte_count + 1.0),
            "mean_packet_len": mean_len,
            "std_packet_len": math.sqrt(len_var),
            "min_packet_len": self.min_len if self.min_len != 2**31 - 1 else 0,
            "max_packet_len": self.max_len,
            "mean_iat": mean_iat,
            "std_iat": math.sqrt(iat_var),
            "min_iat": 0.0 if math.isinf(self.iat_min) else self.iat_min,
            "max_iat": self.iat_max,
            "encrypted_packet_count": encrypted_packets,
            "encrypted_packet_ratio": encrypted_packets / self.packet_count if self.packet_count else 0.0,
            "protocol_counts": json.dumps(dict(sorted(self.protocol_counts.items())), ensure_ascii=False),
            "encryption_counts": json.dumps(dict(sorted(self.encryption_counts.items())), ensure_ascii=False),
            "sequence_text": " ".join(self.sequence_tokens),
        }


def iter_capture_files(paths: Iterable[Path]) -> list[Path]:
    capture_files: list[Path] = []
    for path in paths:
        if path.is_dir():
            capture_files.extend(
                file for file in sorted(path.rglob("*")) if file.is_file() and file.suffix.lower() in CAPTURE_EXTENSIONS
            )
        elif path.is_file() and path.suffix.lower() in CAPTURE_EXTENSIONS:
            capture_files.append(path)
        else:
            raise FileNotFoundError(f"Unsupported capture source: {path}")
    return sorted(capture_files)


def run_tshark_fields(capture_path: Path) -> subprocess.Popen:
    command = [
        "tshark",
        "-r",
        str(capture_path),
        "-T",
        "fields",
        "-E",
        "separator=\t",
        "-e",
        "frame.time_epoch",
        "-e",
        "frame.len",
        "-e",
        "ip.src",
        "-e",
        "ipv6.src",
        "-e",
        "ip.dst",
        "-e",
        "ipv6.dst",
        "-e",
        "tcp.srcport",
        "-e",
        "tcp.dstport",
        "-e",
        "udp.srcport",
        "-e",
        "udp.dstport",
        "-e",
        "_ws.col.Protocol",
    ]
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def process_capture(
    capture_path: Path,
    max_sequence_packets: int,
) -> tuple[list[FlowStats], dict[str, object]]:
    source_group = classify_source_group(capture_path)
    business_hint = infer_business_hint(capture_path)
    capture_name = capture_path.name
    flows: dict[tuple[str, tuple[str, str], tuple[str, str]], FlowStats] = {}
    packet_count = 0
    skipped_packets = 0
    capture_protocol_counts: Counter[str] = Counter()
    capture_encryption_counts: Counter[str] = Counter()

    process = run_tshark_fields(capture_path)
    assert process.stdout is not None

    for raw_line in process.stdout:
        fields = raw_line.rstrip("\n").split("\t")
        if len(fields) < 11:
            fields.extend([""] * (11 - len(fields)))
        timestamp = to_float(fields[0], default=0.0)
        length = to_int(fields[1], default=0)
        src = first_value(fields[2]) or first_value(fields[3])
        dst = first_value(fields[4]) or first_value(fields[5])
        tcp_sport = first_value(fields[6])
        tcp_dport = first_value(fields[7])
        udp_sport = first_value(fields[8])
        udp_dport = first_value(fields[9])
        protocol = first_value(fields[10]) or "UNKNOWN"

        if tcp_sport or tcp_dport:
            transport = "TCP"
            sport = tcp_sport
            dport = tcp_dport
        elif udp_sport or udp_dport:
            transport = "UDP"
            sport = udp_sport
            dport = udp_dport
        else:
            skipped_packets += 1
            continue

        if not src or not dst or not sport or not dport:
            skipped_packets += 1
            continue

        encryption_label = normalize_protocol(protocol)
        packet_count += 1
        capture_protocol_counts[protocol] += 1
        if encryption_label:
            capture_encryption_counts[encryption_label] += 1

        key = canonical_flow_key(src, dst, sport, dport, transport)
        if key not in flows:
            _, endpoint_a, endpoint_b = key
            flows[key] = FlowStats(
                capture_path=str(capture_path),
                capture_name=capture_name,
                source_group=source_group,
                business_hint=business_hint,
                transport=transport,
                endpoint_a_ip=endpoint_a[0],
                endpoint_a_port=endpoint_a[1],
                endpoint_b_ip=endpoint_b[0],
                endpoint_b_port=endpoint_b[1],
                first_time=timestamp,
                last_time=timestamp,
            )
        flows[key].update(
            timestamp=timestamp,
            length=length,
            protocol=protocol,
            encryption_label=encryption_label,
            src=src,
            sport=sport,
            max_sequence_packets=max_sequence_packets,
        )

    _, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"tshark failed for {capture_path}:\n{stderr}")

    summary = {
        "capture_name": capture_name,
        "capture_path": str(capture_path),
        "source_group": source_group,
        "business_hint": business_hint,
        "packets_used": packet_count,
        "packets_skipped": skipped_packets,
        "flows_total": len(flows),
        "protocol_counts": dict(sorted(capture_protocol_counts.items())),
        "encryption_counts": dict(sorted(capture_encryption_counts.items())),
    }
    return list(flows.values()), summary


def assign_simple_splits(rows: list[dict[str, object]], seed: int) -> None:
    try:
        import random

        rng = random.Random(seed)
        by_label: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in rows:
            by_label[str(row["encryption_method"])].append(row)

        for label_rows in by_label.values():
            rng.shuffle(label_rows)
            total = len(label_rows)
            if total < 5:
                for row in label_rows:
                    row["split"] = "train"
                continue
            train_end = max(1, int(total * 0.70))
            valid_end = max(train_end + 1, int(total * 0.85))
            valid_end = min(valid_end, total)
            for index, row in enumerate(label_rows):
                if index < train_end:
                    row["split"] = "train"
                elif index < valid_end:
                    row["split"] = "valid"
                else:
                    row["split"] = "test"
    except Exception:
        for row in rows:
            row["split"] = "train"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_sequence_tsv(path: Path, rows: list[dict[str, object]], label_to_id: dict[str, int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text_a", "label", "flow_id"], delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "text_a": row["sequence_text"],
                    "label": label_to_id[str(row["encryption_method"])],
                    "flow_id": row["flow_id"],
                }
            )


def write_vocab(path: Path, rows: list[dict[str, object]]) -> None:
    tokens = {"[PAD]", "[UNK]", "[SEP]"}
    for row in rows:
        tokens.update(str(row["sequence_text"]).split())
    ordered = ["[PAD]", "[UNK]", "[SEP]"] + sorted(tokens - {"[PAD]", "[UNK]", "[SEP]"})
    path.write_text("\n".join(ordered) + "\n", encoding="utf-8")


def write_readme(path: Path, summary: dict[str, object]) -> None:
    content = f"""# Encryption Method Identification Dataset

Generated by `tools/build_encryption_method_dataset.py`.

This is a first-pass dataset for the new research direction: identifying the
visible encryption protocol or encrypted transport mechanism used by traffic.
Labels are derived from tshark protocol dissection, not from business labels.

## Files

- `flow_features_all.csv`: all bidirectional TCP/UDP flows extracted from the selected PCAP files.
- `flow_features_labeled.csv`: flows whose visible protocol label is one of TLS, QUIC, SSH, DTLS, OpenVPN, or WireGuard.
- `packet_sequences.tsv`: simple packet-length/IAT sequence representation for labeled flows.
- `sequence_vocab.txt`: vocabulary for `packet_sequences.tsv`.
- `label_map.json`: mapping from label name to integer id.
- `capture_summary.csv`: per-capture packet and flow summary.
- `dataset_summary.json`: global summary and processing configuration.

## Current Scope

- Capture files processed: {summary["captures_processed"]}
- Labeled flows: {summary["labeled_flows"]}
- All flows: {summary["all_flows"]}

Important: this version uses visible protocol labels reported by tshark. It is
appropriate for TLS/QUIC/SSH/DTLS-style protocol identification. The current
local ISCX VPN files mostly expose the traffic inside the VPN tunnel, so file
names containing `vpn_` are treated as source metadata rather than direct
OpenVPN/WireGuard labels.
"""
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build encryption-method flow features from PCAP files.")
    parser.add_argument(
        "--sources",
        nargs="+",
        default=["data/NonVPN-PCAPs-01", "data/NonVPN-PCAPs-03", "data/VPN-PCAPs-02"],
        help="PCAP/PCAPNG files or directories to process.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output dataset directory under data/.",
    )
    parser.add_argument("--min-packets", type=int, default=3, help="Minimum packets per labeled flow.")
    parser.add_argument(
        "--min-class-flows",
        type=int,
        default=5,
        help="Minimum number of labeled flows required to keep a class in the training-ready dataset.",
    )
    parser.add_argument("--max-sequence-packets", type=int, default=64, help="Packets kept in sequence text.")
    parser.add_argument("--seed", type=int, default=42, help="Seed used for simple row-level splits.")
    parser.add_argument("--max-captures", type=int, default=0, help="Optional limit for quick smoke runs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if shutil.which("tshark") is None:
        raise FileNotFoundError("tshark was not found in PATH. Install Wireshark or add tshark to PATH.")

    source_paths = [Path(source) for source in args.sources]
    for source in source_paths:
        if not source.exists():
            raise FileNotFoundError(f"Source does not exist: {source}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    capture_files = iter_capture_files(source_paths)
    if args.max_captures > 0:
        capture_files = capture_files[: args.max_captures]
    if not capture_files:
        raise ValueError("No capture files found.")

    all_flow_objects: list[FlowStats] = []
    capture_summaries: list[dict[str, object]] = []

    print(f"Processing {len(capture_files)} capture files...")
    for index, capture_path in enumerate(capture_files, start=1):
        print(f"[{index}/{len(capture_files)}] {capture_path}")
        flows, summary = process_capture(capture_path, max_sequence_packets=args.max_sequence_packets)
        all_flow_objects.extend(flows)
        capture_summaries.append(summary)

    all_rows = [flow.to_row(flow_id=index) for index, flow in enumerate(all_flow_objects)]
    labeled_rows = [
        row
        for row in all_rows
        if row["encryption_method"] != UNKNOWN_LABEL and int(row["packet_count"]) >= args.min_packets
    ]
    raw_label_counts = Counter(str(row["encryption_method"]) for row in labeled_rows)
    dropped_small_classes = {
        label: count for label, count in raw_label_counts.items() if count < args.min_class_flows
    }
    if dropped_small_classes:
        labeled_rows = [
            row for row in labeled_rows if raw_label_counts[str(row["encryption_method"])] >= args.min_class_flows
        ]
    assign_simple_splits(labeled_rows, seed=args.seed)

    label_names = sorted({str(row["encryption_method"]) for row in labeled_rows})
    label_to_id = {label: index for index, label in enumerate(label_names)}

    capture_rows = []
    for item in capture_summaries:
        capture_rows.append(
            {
                "capture_name": item["capture_name"],
                "capture_path": item["capture_path"],
                "source_group": item["source_group"],
                "business_hint": item["business_hint"],
                "packets_used": item["packets_used"],
                "packets_skipped": item["packets_skipped"],
                "flows_total": item["flows_total"],
                "protocol_counts": json.dumps(item["protocol_counts"], ensure_ascii=False),
                "encryption_counts": json.dumps(item["encryption_counts"], ensure_ascii=False),
            }
        )

    write_csv(output_dir / "flow_features_all.csv", all_rows)
    write_csv(output_dir / "flow_features_labeled.csv", labeled_rows)
    write_csv(output_dir / "capture_summary.csv", capture_rows)
    write_sequence_tsv(output_dir / "packet_sequences.tsv", labeled_rows, label_to_id)
    write_vocab(output_dir / "sequence_vocab.txt", labeled_rows)
    (output_dir / "label_map.json").write_text(
        json.dumps(label_to_id, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    label_counts = Counter(str(row["encryption_method"]) for row in labeled_rows)
    split_counts = Counter(str(row.get("split", "train")) for row in labeled_rows)
    summary = {
        "sources": [str(source) for source in source_paths],
        "output_dir": str(output_dir),
        "captures_processed": len(capture_files),
        "all_flows": len(all_rows),
        "labeled_flows": len(labeled_rows),
        "unknown_or_non_encrypted_flows": len(all_rows) - len(labeled_rows),
        "min_packets": args.min_packets,
        "min_class_flows": args.min_class_flows,
        "max_sequence_packets": args.max_sequence_packets,
        "label_counts": dict(sorted(label_counts.items())),
        "dropped_small_classes": dict(sorted(dropped_small_classes.items())),
        "split_counts": dict(sorted(split_counts.items())),
        "label_map": label_to_id,
        "note": (
            "Labels are derived from visible tshark protocol names. VPN file names are source metadata only "
            "because the current local VPN captures mostly expose inner traffic rather than outer VPN tunnels."
        ),
    }
    (output_dir / "dataset_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_readme(output_dir / "README.md", summary)

    print("Dataset build finished.")
    print(f"Output directory : {output_dir}")
    print(f"All flows        : {summary['all_flows']}")
    print(f"Labeled flows    : {summary['labeled_flows']}")
    print(f"Labels           : {summary['label_counts']}")


if __name__ == "__main__":
    main()
