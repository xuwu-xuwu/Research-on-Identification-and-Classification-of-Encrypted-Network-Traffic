#!/usr/bin/env python
"""Build a paper-method benchmark for encryption-method identification.

The first-layer main table uses full tabular data. This script builds the
second-layer benchmark required by packet/sequence papers such as ET-BERT,
TFE-GNN, and Deep Packet. Every exported sample is a flow reconstructed from
real PCAP packets, not a synthetic vector derived from `sequence_text`.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from scapy.all import IP, IPv6, TCP, UDP
from scapy.utils import PcapNgReader, PcapReader

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.encryption_method.unified_benchmark_utils import COMMON_NUMERIC_FEATURES
from src.encryption_method.packet_encoding_utils import (
    bigram_generation,
    extract_paper_bytes,
    pad_or_truncate,
)


LABELS = ["NON_ENCRYPTED", "TLS_FAMILY", "SSH", "QUIC", "TOR"]
FLOW_LABEL_MAP = {
    "TLS": "TLS_FAMILY",
    "DTLS": "TLS_FAMILY",
    "SSH": "SSH",
    "QUIC": "QUIC",
}
CAPTURE_EXTENSIONS = {".pcap", ".pcapng"}
COMMON_ENCRYPTED_PORTS = {22, 443, 465, 853, 993, 995, 1194, 51820, 8443, 9443}
TOR_PORTS = {443, 9001, 9030, 9040, 9050, 9051, 9150, 9151}


@dataclass(frozen=True)
class FlowKey:
    transport: str
    endpoint_a_ip: str
    endpoint_a_port: str
    endpoint_b_ip: str
    endpoint_b_port: str

    def as_text(self) -> str:
        return "|".join(
            [
                self.transport,
                self.endpoint_a_ip,
                self.endpoint_a_port,
                self.endpoint_b_ip,
                self.endpoint_b_port,
            ]
        )


@dataclass
class PacketRecord:
    timestamp: float
    length: int
    raw_bytes: bytes
    full_bytes: bytes
    direction: str


@dataclass
class FlowPacketBuffer:
    capture_path: Path
    key: FlowKey
    packets: list[PacketRecord] = field(default_factory=list)

    def add_packet(self, packet, timestamp: float, length: int, direction: str) -> None:
        retained = extract_paper_bytes(packet)
        if retained is None:
            return
        self.packets.append(
            PacketRecord(
                timestamp=timestamp,
                length=length,
                raw_bytes=retained,
                full_bytes=bytes(packet),
                direction=direction,
            )
        )

    @property
    def packet_count(self) -> int:
        return len(self.packets)

    @property
    def byte_count(self) -> int:
        return int(sum(packet.length for packet in self.packets))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build 5-class PCAP-based paper-method benchmark.")
    parser.add_argument(
        "--flow-labeled-csv",
        default="data/encryption_method_identification/flow_features_labeled.csv",
        help="Flow labels with capture path and endpoints for TLS/SSH/QUIC.",
    )
    parser.add_argument("--nontor-dir", default="data/NonTor/NonTor", help="Raw NonTor PCAP directory.")
    parser.add_argument("--tor-dir", default="data/Tor/Tor", help="Raw Tor PCAP directory.")
    parser.add_argument(
        "--output-dir",
        default="data/paper_benchmark/encryption_method_5class_pcap_v1",
        help="Output benchmark directory.",
    )
    parser.add_argument("--max-flows-per-label", type=int, default=160, help="Class cap for a balanced local benchmark.")
    parser.add_argument("--max-packets-per-flow", type=int, default=6, help="Packets retained per flow sample.")
    parser.add_argument("--packet-size", type=int, default=256, help="Bytes retained per packet for neural baselines.")
    parser.add_argument("--trafficformer-packet-len", type=int, default=64, help="Bytes retained per packet for hex tokens.")
    parser.add_argument("--trafficformer-start-index", type=int, default=28, help="Hex-byte offset used by TrafficFormer.")
    parser.add_argument("--min-packets", type=int, default=4, help="Minimum packets for auto-labeled raw flows.")
    parser.add_argument("--min-bytes", type=int, default=256, help="Minimum bytes for auto-labeled raw flows.")
    parser.add_argument("--max-capture-packets", type=int, default=20000, help="Maximum packets read from one capture.")
    parser.add_argument("--max-auto-captures-per-label", type=int, default=8, help="Raw captures scanned for NON/TOR labels.")
    parser.add_argument("--max-capture-paths-per-label", type=int, default=8, help="Richest labeled capture paths kept per label.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def iter_capture_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in CAPTURE_EXTENSIONS)


def canonical_key(src: str, dst: str, sport: str, dport: str, transport: str) -> FlowKey:
    endpoint_a = (src, sport)
    endpoint_b = (dst, dport)
    if endpoint_b < endpoint_a:
        endpoint_a, endpoint_b = endpoint_b, endpoint_a
    return FlowKey(
        transport=transport,
        endpoint_a_ip=endpoint_a[0],
        endpoint_a_port=endpoint_a[1],
        endpoint_b_ip=endpoint_b[0],
        endpoint_b_port=endpoint_b[1],
    )


def packet_key(packet) -> tuple[FlowKey, str] | None:
    if IP in packet:
        src = str(packet[IP].src)
        dst = str(packet[IP].dst)
    elif IPv6 in packet:
        src = str(packet[IPv6].src)
        dst = str(packet[IPv6].dst)
    else:
        return None

    if TCP in packet:
        transport = "TCP"
        sport = str(int(packet[TCP].sport))
        dport = str(int(packet[TCP].dport))
    elif UDP in packet:
        transport = "UDP"
        sport = str(int(packet[UDP].sport))
        dport = str(int(packet[UDP].dport))
    else:
        return None

    key = canonical_key(src=src, dst=dst, sport=sport, dport=dport, transport=transport)
    direction = "F" if (src, sport) == (key.endpoint_a_ip, key.endpoint_a_port) else "B"
    return key, direction


def read_capture_flows(
    capture_path: Path,
    wanted_keys: set[FlowKey] | None = None,
    max_packets: int = 0,
) -> dict[FlowKey, FlowPacketBuffer]:
    reader_cls = PcapNgReader if capture_path.suffix.lower() == ".pcapng" else PcapReader
    flows: dict[FlowKey, FlowPacketBuffer] = {}
    reader = reader_cls(str(capture_path))
    try:
        for packet_index, packet in enumerate(reader, start=1):
            if max_packets > 0 and packet_index > max_packets:
                break
            key_direction = packet_key(packet)
            if key_direction is None:
                continue
            key, direction = key_direction
            if wanted_keys is not None and key not in wanted_keys:
                continue
            flow = flows.get(key)
            if flow is None:
                flow = FlowPacketBuffer(capture_path=capture_path, key=key)
                flows[key] = flow
            timestamp = float(getattr(packet, "time", 0.0))
            length = int(len(packet))
            flow.add_packet(packet=packet, timestamp=timestamp, length=length, direction=direction)
    finally:
        reader.close()
    return flows


def row_to_key(row: pd.Series) -> FlowKey:
    return canonical_key(
        src=str(row["endpoint_a_ip"]),
        dst=str(row["endpoint_b_ip"]),
        sport=str(int(float(row["endpoint_a_port"]))),
        dport=str(int(float(row["endpoint_b_port"]))),
        transport=str(row["transport"]).upper(),
    )


def stable_split(label: str, capture_path: Path, key: FlowKey) -> str:
    digest = hashlib.sha1(f"{label}|{capture_path}|{key.as_text()}".encode("utf-8")).hexdigest()
    value = int(digest[:8], 16) / 0xFFFFFFFF
    if value < 0.70:
        return "train"
    if value < 0.85:
        return "valid"
    return "test"


def packet_iats(packets: list[PacketRecord]) -> list[float]:
    if not packets:
        return []
    iats = [0.0]
    for previous, current in zip(packets, packets[1:]):
        iats.append(max(current.timestamp - previous.timestamp, 0.0))
    return iats


def flow_numeric_features(flow: FlowPacketBuffer) -> dict[str, float]:
    packets = flow.packets
    lengths = np.asarray([packet.length for packet in packets], dtype=np.float64)
    iats = np.asarray(packet_iats(packets)[1:], dtype=np.float64)
    directions = [packet.direction for packet in packets]
    fwd_mask = np.asarray([direction == "F" for direction in directions], dtype=bool)
    bwd_mask = ~fwd_mask
    duration = max(packets[-1].timestamp - packets[0].timestamp, 0.0) if len(packets) > 1 else 0.0

    fwd_packet_count = int(fwd_mask.sum())
    bwd_packet_count = int(bwd_mask.sum())
    fwd_byte_count = int(lengths[fwd_mask].sum()) if fwd_packet_count else 0
    bwd_byte_count = int(lengths[bwd_mask].sum()) if bwd_packet_count else 0
    packet_count = int(len(packets))
    byte_count = int(lengths.sum()) if len(lengths) else 0

    return {
        "duration": float(duration),
        "packet_count": float(packet_count),
        "fwd_packet_count": float(fwd_packet_count),
        "bwd_packet_count": float(bwd_packet_count),
        "byte_count": float(byte_count),
        "fwd_byte_count": float(fwd_byte_count),
        "bwd_byte_count": float(bwd_byte_count),
        "packets_per_second": float(packet_count / (duration + 1e-9)),
        "bytes_per_second": float(byte_count / (duration + 1e-9)),
        "mean_packet_len": float(lengths.mean()) if len(lengths) else 0.0,
        "std_packet_len": float(lengths.std()) if len(lengths) else 0.0,
        "min_packet_len": float(lengths.min()) if len(lengths) else 0.0,
        "max_packet_len": float(lengths.max()) if len(lengths) else 0.0,
        "mean_iat": float(iats.mean()) if len(iats) else 0.0,
        "std_iat": float(iats.std()) if len(iats) else 0.0,
        "min_iat": float(iats.min()) if len(iats) else 0.0,
        "max_iat": float(iats.max()) if len(iats) else 0.0,
        "direction_packet_ratio": float(fwd_packet_count / (bwd_packet_count + 1.0)),
        "direction_byte_ratio": float(fwd_byte_count / (bwd_byte_count + 1.0)),
        "avg_packet_size": float(lengths.mean()) if len(lengths) else 0.0,
        "encrypted_packet_ratio": 0.0,
    }


def sequence_text(flow: FlowPacketBuffer, max_packets: int) -> str:
    tokens: list[str] = []
    iats = packet_iats(flow.packets)
    for packet, iat in zip(flow.packets[:max_packets], iats[:max_packets]):
        direction = packet.direction
        length_bucket = int(round(min(max(packet.length, 0), 2000) / 50.0) * 50)
        milliseconds = min(max(iat * 1000.0, 0.0), 10000.0)
        iat_bucket = int(round(milliseconds / 100.0) * 100) if milliseconds > 100 else int(round(milliseconds))
        tokens.append(f"{direction}_LEN_{length_bucket:04d}")
        tokens.append(f"IAT_{iat_bucket:05d}")
    return " ".join(tokens)


def trafficformer_text(flow: FlowPacketBuffer, max_packets: int, packet_len: int, start_index: int) -> str:
    packet_chunks: list[str] = []
    for packet in flow.packets[:max_packets]:
        packet_hex = packet.full_bytes.hex()
        packet_hex = packet_hex[start_index : start_index + 2 * packet_len]
        if not packet_hex:
            continue
        chunk = bigram_generation(packet_hex.strip(), token_len=len(packet_hex.strip()), flag=True).strip()
        if chunk:
            packet_chunks.append("[SEP] " + chunk)
    return " ".join(packet_chunks).strip()


def packet_tensor(flow: FlowPacketBuffer, max_packets: int, packet_size: int) -> np.ndarray:
    rows = [pad_or_truncate(packet.raw_bytes, packet_size=packet_size) for packet in flow.packets[:max_packets]]
    while len(rows) < max_packets:
        rows.append(np.zeros(packet_size, dtype=np.uint8))
    return np.stack(rows).astype(np.uint8, copy=False)


def has_encrypted_port(key: FlowKey) -> bool:
    ports = {int(key.endpoint_a_port), int(key.endpoint_b_port)}
    return bool(ports & COMMON_ENCRYPTED_PORTS)


def load_labeled_flow_specs(path: Path, max_per_label: int, max_capture_paths_per_label: int) -> dict[Path, list[dict[str, object]]]:
    raw = pd.read_csv(path, low_memory=False)
    raw = raw.loc[raw["encryption_method"].astype(str).str.upper().isin(FLOW_LABEL_MAP)].copy()
    raw["final_label"] = raw["encryption_method"].astype(str).str.upper().map(FLOW_LABEL_MAP)
    ordered_frames = []
    for label, group in raw.groupby("final_label", sort=False):
        top_paths = group["capture_path"].value_counts().head(max_capture_paths_per_label).index.tolist()
        label_group = group.loc[group["capture_path"].isin(top_paths)].sort_values(["capture_path", "flow_id"])
        ordered_frames.append(label_group.head(max_per_label * 3))
    raw = pd.concat(ordered_frames, ignore_index=True)

    grouped: dict[Path, list[dict[str, object]]] = defaultdict(list)
    for _, row in raw.iterrows():
        capture_path = Path(str(row["capture_path"]))
        key = row_to_key(row)
        grouped[capture_path].append(
            {
                "label": str(row["final_label"]),
                "split": str(row["split"]),
                "key": key,
                "source": "FLOW_LABELED",
            }
        )
    return grouped


def append_flow_sample(
    samples: list[dict[str, object]],
    flow: FlowPacketBuffer,
    label: str,
    split: str,
    source: str,
    args: argparse.Namespace,
) -> None:
    if flow.packet_count < args.min_packets or flow.byte_count < args.min_bytes:
        return
    samples.append(
        {
            "label": label,
            "split": split,
            "source": source,
            "capture_path": str(flow.capture_path),
            "capture_name": flow.capture_path.name,
            "flow_key": flow.key.as_text(),
            "transport": flow.key.transport,
            "packet_count": flow.packet_count,
            "byte_count": flow.byte_count,
            "packet_tensor": packet_tensor(flow, args.max_packets_per_flow, args.packet_size),
            "first_packet": pad_or_truncate(flow.packets[0].raw_bytes, packet_size=args.packet_size),
            "trafficformer_text": trafficformer_text(
                flow,
                max_packets=args.max_packets_per_flow,
                packet_len=args.trafficformer_packet_len,
                start_index=args.trafficformer_start_index,
            ),
            "sequence_text": sequence_text(flow, args.max_packets_per_flow),
            "numeric_features": flow_numeric_features(flow),
        }
    )


def collect_labeled_samples(args: argparse.Namespace, counts: Counter[str]) -> list[dict[str, object]]:
    specs_by_capture = load_labeled_flow_specs(
        Path(args.flow_labeled_csv),
        max_per_label=args.max_flows_per_label,
        max_capture_paths_per_label=args.max_capture_paths_per_label,
    )
    samples: list[dict[str, object]] = []

    for capture_path, specs in sorted(specs_by_capture.items(), key=lambda item: str(item[0])):
        wanted = {spec["key"] for spec in specs if counts[str(spec["label"])] < args.max_flows_per_label}
        if not wanted or not capture_path.exists():
            continue
        flows = read_capture_flows(capture_path, wanted_keys=wanted, max_packets=args.max_capture_packets)
        for spec in specs:
            label = str(spec["label"])
            if counts[label] >= args.max_flows_per_label:
                continue
            flow = flows.get(spec["key"])
            if flow is None:
                continue
            before = len(samples)
            append_flow_sample(samples, flow, label, str(spec["split"]), str(spec["source"]), args)
            if len(samples) > before:
                counts[label] += 1
    return samples


def collect_auto_samples(
    args: argparse.Namespace,
    root: Path,
    label: str,
    source: str,
    counts: Counter[str],
) -> list[dict[str, object]]:
    samples: list[dict[str, object]] = []
    for capture_index, capture_path in enumerate(iter_capture_files(root), start=1):
        if capture_index > args.max_auto_captures_per_label:
            break
        if counts[label] >= args.max_flows_per_label:
            break
        flows = read_capture_flows(capture_path, wanted_keys=None, max_packets=args.max_capture_packets)
        for flow in sorted(flows.values(), key=lambda item: (-item.byte_count, item.key.as_text())):
            if counts[label] >= args.max_flows_per_label:
                break
            if flow.packet_count < args.min_packets or flow.byte_count < args.min_bytes:
                continue

            if label == "NON_ENCRYPTED" and has_encrypted_port(flow.key):
                continue
            if label == "TOR":
                ports = {int(flow.key.endpoint_a_port), int(flow.key.endpoint_b_port)}
                if flow.key.transport != "TCP" or not ((ports & TOR_PORTS) or flow.byte_count >= 1024):
                    continue

            split = stable_split(label, capture_path, flow.key)
            before = len(samples)
            append_flow_sample(samples, flow, label, split, source, args)
            if len(samples) > before:
                counts[label] += 1
    return samples


def write_tsv(rows: list[dict[str, object]], label_map: dict[str, int], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "text_a"], delimiter="\t")
        writer.writeheader()
        for row in rows:
            text = str(row["trafficformer_text"]).strip()
            if text:
                writer.writerow({"label": label_map[str(row["label"])], "text_a": text})


def write_vocab(tsv_dir: Path, output_path: Path) -> None:
    tokens = {"[PAD]", "[UNK]", "[SEP]", "[CLS]", "[MASK]"}
    for tsv_path in [tsv_dir / "train_dataset.tsv", tsv_dir / "valid_dataset.tsv", tsv_dir / "test_dataset.tsv"]:
        with tsv_path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                tokens.update(str(row["text_a"]).split())
    output_path.write_text("\n".join(sorted(tokens)) + "\n", encoding="utf-8")


def split_rows(samples: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    return {
        split: [row for row in samples if row["split"] == split]
        for split in ("train", "valid", "test")
    }


def write_hybrid_dataset(samples: list[dict[str, object]], label_names: list[str], output_dir: Path) -> None:
    rows: list[dict[str, object]] = []
    for index, sample in enumerate(samples):
        label = str(sample["label"])
        row = {
            "source_name": "PAPER_PCAP_5CLASS",
            "sample_id": index,
            "split": sample["split"],
            "transport": sample["transport"],
            "sequence_text": sample["sequence_text"],
            "binary_label": "NON_ENCRYPTED" if label == "NON_ENCRYPTED" else "ENCRYPTED",
            "final_label": label,
            "raw_label": sample["source"],
        }
        row.update(sample["numeric_features"])
        rows.append(row)

    frame = pd.DataFrame(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_dir / "multiclass_finetune.csv", index=False)
    frame.to_csv(output_dir / "binary_pretrain.csv", index=False)
    metadata = {
        "common_numeric_features": COMMON_NUMERIC_FEATURES,
        "binary_label_order": ["NON_ENCRYPTED", "ENCRYPTED"],
        "final_label_order": label_names,
        "source": "paper_pcap_5class_benchmark",
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    counts: Counter[str] = Counter()
    samples: list[dict[str, object]] = []
    samples.extend(collect_labeled_samples(args, counts))
    samples.extend(collect_auto_samples(args, Path(args.nontor_dir), "NON_ENCRYPTED", "RAW_NONTOR_AUTO", counts))
    samples.extend(collect_auto_samples(args, Path(args.tor_dir), "TOR", "RAW_TOR_AUTO", counts))

    samples = [sample for sample in samples if str(sample["trafficformer_text"]).strip()]
    label_names = [label for label in LABELS if any(sample["label"] == label for sample in samples)]
    label_map = {label: index for index, label in enumerate(label_names)}

    if len(label_names) < len(LABELS):
        missing = sorted(set(LABELS) - set(label_names))
        raise ValueError(f"Benchmark is missing labels after extraction: {missing}")

    y = np.asarray([label_map[str(sample["label"])] for sample in samples], dtype=np.int64)
    split_names = np.asarray([str(sample["split"]) for sample in samples], dtype="<U8")
    flow_ids = np.asarray([f"flow_{index:06d}" for index in range(len(samples))], dtype="<U32")
    flow_bytes = np.stack([sample["packet_tensor"] for sample in samples]).astype(np.uint8, copy=False)
    first_packets = np.stack([sample["first_packet"] for sample in samples]).astype(np.uint8, copy=False)

    packet_dir = output_dir / "packet"
    packet_dir.mkdir(parents=True, exist_ok=True)
    importlib.reload(zipfile)
    np.savez_compressed(
        packet_dir / "flows_5class.npz",
        x=flow_bytes,
        x_first=first_packets,
        y=y,
        split=split_names,
        labels=np.asarray(label_names, dtype="<U32"),
        flow_ids=flow_ids,
    )

    split_to_rows = split_rows(samples)
    tsv_dir = output_dir / "trafficformer"
    write_tsv(split_to_rows["train"], label_map, tsv_dir / "train_dataset.tsv")
    write_tsv(split_to_rows["valid"], label_map, tsv_dir / "valid_dataset.tsv")
    write_tsv(split_to_rows["test"], label_map, tsv_dir / "test_dataset.tsv")
    (tsv_dir / "label_map.json").write_text(json.dumps(label_map, indent=2, ensure_ascii=False), encoding="utf-8")
    write_vocab(tsv_dir, tsv_dir / "vocab.txt")

    metadata_rows = []
    for index, sample in enumerate(samples):
        metadata_rows.append(
            {
                "flow_id": flow_ids[index],
                "label": sample["label"],
                "label_id": int(y[index]),
                "split": sample["split"],
                "source": sample["source"],
                "capture_path": sample["capture_path"],
                "capture_name": sample["capture_name"],
                "flow_key": sample["flow_key"],
                "transport": sample["transport"],
                "packet_count": sample["packet_count"],
                "byte_count": sample["byte_count"],
            }
        )
    pd.DataFrame(metadata_rows).to_csv(output_dir / "metadata.csv", index=False)
    write_hybrid_dataset(samples, label_names, output_dir / "hybrid")

    summary = {
        "benchmark_name": "encryption_method_5class_pcap_v1",
        "label_names": label_names,
        "label_map": label_map,
        "samples_total": int(len(samples)),
        "samples_by_label": dict(Counter(sample["label"] for sample in samples)),
        "samples_by_split": dict(Counter(sample["split"] for sample in samples)),
        "samples_by_source": dict(Counter(sample["source"] for sample in samples)),
        "max_flows_per_label": args.max_flows_per_label,
        "max_packets_per_flow": args.max_packets_per_flow,
        "packet_size": args.packet_size,
        "outputs": {
            "packet_npz": str(packet_dir / "flows_5class.npz"),
            "trafficformer_dir": str(tsv_dir),
            "hybrid_dir": str(output_dir / "hybrid"),
        },
    }
    (output_dir / "dataset_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Paper-method benchmark build finished.")
    print(f"Output dir       : {output_dir}")
    print(f"Samples total    : {len(samples)}")
    print(f"Samples by label : {summary['samples_by_label']}")
    print(f"Samples by split : {summary['samples_by_split']}")


if __name__ == "__main__":
    main()
