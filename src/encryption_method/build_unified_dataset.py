#!/usr/bin/env python
"""Build a unified encryption-method dataset from multiple local sources.

This script is written from scratch for the encryption-method pivot. It reads
all cleanly mappable datasets under data/, aligns them to a shared feature
schema, assigns consistent train/valid/test splits, and writes two outputs:

1. binary_pretrain.csv
   - coarse labels: ENCRYPTED vs NON_ENCRYPTED
2. multiclass_finetune.csv
   - final labels for encryption-method identification
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

COMMON_NUMERIC_FEATURES = [
    "duration",
    "packet_count",
    "fwd_packet_count",
    "bwd_packet_count",
    "byte_count",
    "fwd_byte_count",
    "bwd_byte_count",
    "packets_per_second",
    "bytes_per_second",
    "mean_packet_len",
    "std_packet_len",
    "min_packet_len",
    "max_packet_len",
    "mean_iat",
    "std_iat",
    "min_iat",
    "max_iat",
    "direction_packet_ratio",
    "direction_byte_ratio",
    "avg_packet_size",
    "encrypted_packet_ratio",
]

FINAL_LABEL_ORDER = [
    "NON_ENCRYPTED",
    "TLS_FAMILY",
    "SSH",
    "QUIC",
    "VPN",
    "TOR",
    "I2P",
    "FREENET",
    "ZERONET",
]

BINARY_LABEL_ORDER = [
    "NON_ENCRYPTED",
    "ENCRYPTED",
]

RAW_CAPTURE_EXTENSIONS = {".pcap", ".pcapng"}
TOR_PORTS = {443, 9001, 9030, 9040, 9050, 9051, 9150, 9151}
ENCRYPTED_PROTOCOL_HINTS = {"TLS_FAMILY", "SSH", "QUIC"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build unified encryption-method datasets.")
    parser.add_argument(
        "--dataset-csv",
        default="data/Dataset.csv",
        help="Path to Dataset.csv.",
    )
    parser.add_argument(
        "--bccc-binary-csv",
        default="data/BCCC-Darknet-2025 (6)(1)/Binary -2DSCombined.csv",
        help="Path to BCCC binary dataset.",
    )
    parser.add_argument(
        "--bccc-multiclass-csv",
        default="data/BCCC-Darknet-2025 (6)(1)/MultiTotalDS.csv",
        help="Path to BCCC multiclass dataset.",
    )
    parser.add_argument(
        "--flow-all-csv",
        default="data/encryption_method_identification/flow_features_all.csv",
        help="Path to all flow features csv.",
    )
    parser.add_argument(
        "--flow-labeled-csv",
        default="data/encryption_method_identification/flow_features_labeled.csv",
        help="Path to labeled flow features csv.",
    )
    parser.add_argument(
        "--tor-dir",
        default="data/Tor/Tor",
        help="Path to extracted Tor raw capture directory.",
    )
    parser.add_argument(
        "--nontor-dir",
        default="data/NonTor/NonTor",
        help="Path to extracted NonTor raw capture directory.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/unified_encryption_method_v1",
        help="Directory for unified outputs.",
    )
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    parser.add_argument("--raw-min-packets", type=int, default=4, help="Minimum packet count for raw-capture flows.")
    parser.add_argument("--raw-min-bytes", type=int, default=256, help="Minimum byte count for raw-capture flows.")
    parser.add_argument("--raw-max-seq-packets", type=int, default=64, help="Maximum packets to tokenize per raw flow.")
    return parser.parse_args()


def as_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def standardize_transport(value: object) -> str:
    if pd.isna(value):
        return "OTHER"
    text = str(value).strip().upper()
    if text in {"6", "6.0", "TCP"}:
        return "TCP"
    if text in {"17", "17.0", "UDP"}:
        return "UDP"
    return text if text else "OTHER"


def random_split(size: int, seed: int) -> pd.Series:
    rng = np.random.default_rng(seed)
    indices = np.arange(size)
    rng.shuffle(indices)
    train_end = int(size * 0.70)
    valid_end = int(size * 0.85)
    split = np.empty(size, dtype=object)
    split[indices[:train_end]] = "train"
    split[indices[train_end:valid_end]] = "valid"
    split[indices[valid_end:]] = "test"
    return pd.Series(split)


def assign_split(df: pd.DataFrame, label_col: str, seed: int) -> pd.Series:
    labels = df[label_col].astype(str)
    if labels.nunique() < 2:
        return random_split(len(df), seed)

    train_idx, temp_idx = train_test_split(
        df.index.to_numpy(),
        test_size=0.30,
        random_state=seed,
        stratify=labels.to_numpy(),
    )
    temp_labels = labels.loc[temp_idx].to_numpy()
    valid_idx, test_idx = train_test_split(
        temp_idx,
        test_size=0.50,
        random_state=seed,
        stratify=temp_labels,
    )
    split = pd.Series(index=df.index, dtype=object)
    split.loc[train_idx] = "train"
    split.loc[valid_idx] = "valid"
    split.loc[test_idx] = "test"
    return split


def finalize_frame(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    for column in COMMON_NUMERIC_FEATURES:
        if column not in df.columns:
            df[column] = np.nan
        df[column] = as_numeric(df[column])

    df["source_name"] = source_name
    df["transport"] = df.get("transport", "OTHER").map(standardize_transport)
    df["sequence_text"] = df.get("sequence_text", "").fillna("").astype(str)
    df["sample_id"] = np.arange(len(df))

    ordered_columns = [
        "source_name",
        "sample_id",
        "split",
        "transport",
        "sequence_text",
        "binary_label",
        "final_label",
        "raw_label",
    ] + COMMON_NUMERIC_FEATURES
    return df[ordered_columns].copy()


def locate_tshark() -> str:
    candidates = []
    for env_name in ("EIM_TSHARK_PATH", "TSHARK_PATH"):
        env_value = os.getenv(env_name)
        if not env_value:
            continue
        env_path = Path(env_value).expanduser()
        if env_path.is_absolute():
            candidates.append(env_path)
        else:
            candidates.append(Path.cwd() / env_path)
            candidates.append(PROJECT_ROOT / env_path)

    found = shutil.which("tshark")
    if found:
        candidates.append(Path(found))

    if os.name == "nt":
        try:
            import winreg

            for root, subkey in (
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe"),
            ):
                try:
                    with winreg.OpenKey(root, subkey) as key:
                        value, _ = winreg.QueryValueEx(key, None)
                    if value:
                        candidates.append(Path(value))
                except OSError:
                    continue
        except ImportError:
            pass

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate).resolve())
    raise FileNotFoundError("tshark executable not found. Checked EIM_TSHARK_PATH, TSHARK_PATH, PATH, and App Paths.")


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


def safe_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def normalize_tshark_protocol(raw_protocol: str) -> str:
    proto = raw_protocol.upper()
    if "GQUIC" in proto or "QUIC" in proto or "HTTP3" in proto:
        return "QUIC"
    if "SSH" in proto:
        return "SSH"
    if "DTLS" in proto or "TLS" in proto or "SSL" in proto:
        return "TLS_FAMILY"
    if "DNS" in proto:
        return "DNS"
    if "FTP" in proto:
        return "FTP"
    if "HTTP" in proto:
        return "HTTP"
    if "ICMP" in proto:
        return "ICMP"
    if "ARP" in proto:
        return "ARP"
    return "OTHER"


@dataclass
class RawFlowStats:
    capture_name: str
    dataset_name: str
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
    encrypted_packet_count: int = 0
    protocol_counts: Counter[str] = field(default_factory=Counter)
    sequence_tokens: list[str] = field(default_factory=list)

    def update(
        self,
        timestamp: float,
        length: int,
        protocol_name: str,
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
        self.protocol_counts[protocol_name] += 1
        if protocol_name in ENCRYPTED_PROTOCOL_HINTS:
            self.encrypted_packet_count += 1

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

    def to_row(self, raw_label: str, binary_label: str, final_label: str) -> dict[str, object]:
        duration = max(self.last_time - self.first_time, 0.0)
        mean_len = self.sum_len / self.packet_count if self.packet_count else 0.0
        len_var = max((self.sum_len_sq / self.packet_count) - mean_len * mean_len, 0.0) if self.packet_count else 0.0
        mean_iat = self.iat_sum / self.iat_count if self.iat_count else 0.0
        iat_var = max((self.iat_sum_sq / self.iat_count) - mean_iat * mean_iat, 0.0) if self.iat_count else 0.0

        return {
            "raw_label": raw_label,
            "binary_label": binary_label,
            "final_label": final_label,
            "transport": self.transport,
            "sequence_text": " ".join(self.sequence_tokens),
            "duration": duration,
            "packet_count": self.packet_count,
            "fwd_packet_count": self.fwd_packet_count,
            "bwd_packet_count": self.bwd_packet_count,
            "byte_count": self.byte_count,
            "fwd_byte_count": self.fwd_byte_count,
            "bwd_byte_count": self.bwd_byte_count,
            "packets_per_second": self.packet_count / (duration + 1e-9),
            "bytes_per_second": self.byte_count / (duration + 1e-9),
            "mean_packet_len": mean_len,
            "std_packet_len": math.sqrt(len_var),
            "min_packet_len": self.min_len if self.min_len != 2**31 - 1 else 0,
            "max_packet_len": self.max_len,
            "mean_iat": mean_iat,
            "std_iat": math.sqrt(iat_var),
            "min_iat": 0.0 if math.isinf(self.iat_min) else self.iat_min,
            "max_iat": self.iat_max,
            "direction_packet_ratio": self.fwd_packet_count / (self.bwd_packet_count + 1.0),
            "direction_byte_ratio": self.fwd_byte_count / (self.bwd_byte_count + 1.0),
            "avg_packet_size": mean_len,
            "encrypted_packet_ratio": self.encrypted_packet_count / self.packet_count if self.packet_count else 0.0,
            "capture_name": self.capture_name,
        }


def iter_capture_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in RAW_CAPTURE_EXTENSIONS
    )


def run_tshark_fields(tshark_path: str, capture_path: Path) -> subprocess.Popen[str]:
    command = [
        tshark_path,
        "-n",
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


def build_raw_capture_rows(
    capture_path: Path,
    dataset_name: str,
    tshark_path: str,
    min_packets: int,
    min_bytes: int,
    max_sequence_packets: int,
) -> list[dict[str, object]]:
    process = run_tshark_fields(tshark_path, capture_path)
    flows: dict[tuple[str, tuple[str, str], tuple[str, str]], RawFlowStats] = {}
    assert process.stdout is not None
    for raw_line in process.stdout:
        line = raw_line.rstrip("\n\r")
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 11:
            parts.extend([""] * (11 - len(parts)))

        timestamp = safe_float(parts[0])
        length = safe_int(parts[1])
        src = parts[2] or parts[3]
        dst = parts[4] or parts[5]
        tcp_sport = parts[6]
        tcp_dport = parts[7]
        udp_sport = parts[8]
        udp_dport = parts[9]
        protocol_name = normalize_tshark_protocol(parts[10])

        if not src or not dst:
            continue

        if tcp_sport or tcp_dport:
            transport = "TCP"
            sport = tcp_sport
            dport = tcp_dport
        elif udp_sport or udp_dport:
            transport = "UDP"
            sport = udp_sport
            dport = udp_dport
        else:
            continue

        key = canonical_flow_key(src=src, dst=dst, sport=sport, dport=dport, transport=transport)
        flow = flows.get(key)
        if flow is None:
            endpoint_a = key[1]
            endpoint_b = key[2]
            flow = RawFlowStats(
                capture_name=capture_path.name,
                dataset_name=dataset_name,
                transport=transport,
                endpoint_a_ip=endpoint_a[0],
                endpoint_a_port=endpoint_a[1],
                endpoint_b_ip=endpoint_b[0],
                endpoint_b_port=endpoint_b[1],
                first_time=timestamp,
                last_time=timestamp,
            )
            flows[key] = flow
        flow.update(
            timestamp=timestamp,
            length=length,
            protocol_name=protocol_name,
            src=src,
            sport=sport,
            max_sequence_packets=max_sequence_packets,
        )

    stderr_text = ""
    if process.stderr is not None:
        stderr_text = process.stderr.read()
    return_code = process.wait()
    if return_code not in (0, 1):
        if flows:
            print(f"[raw] warning: tshark returned {return_code} for {capture_path.name}, continuing with parsed packets.")
        else:
            raise RuntimeError(f"tshark failed for {capture_path} with code {return_code}: {stderr_text[:500]}")

    rows: list[dict[str, object]] = []
    for flow in flows.values():
        if flow.packet_count < min_packets or flow.byte_count < min_bytes:
            continue

        if dataset_name == "RAW_TOR":
            ports = {safe_int(flow.endpoint_a_port), safe_int(flow.endpoint_b_port)}
            is_tor_like = (
                flow.encrypted_packet_count > 0
                and flow.transport == "TCP"
                and (ports & TOR_PORTS or flow.byte_count >= 1024)
            )
            if not is_tor_like:
                continue
            rows.append(flow.to_row(raw_label="RAW_TOR", binary_label="ENCRYPTED", final_label="TOR"))
            continue

        if flow.protocol_counts["SSH"] > 0 or {safe_int(flow.endpoint_a_port), safe_int(flow.endpoint_b_port)} & {22}:
            final_label = "SSH"
        elif flow.protocol_counts["QUIC"] > 0:
            final_label = "QUIC"
        elif flow.protocol_counts["TLS_FAMILY"] > 0:
            final_label = "TLS_FAMILY"
        else:
            final_label = "NON_ENCRYPTED"

        binary_label = "NON_ENCRYPTED" if final_label == "NON_ENCRYPTED" else "ENCRYPTED"
        rows.append(
            flow.to_row(
                raw_label=f"RAW_NONTOR_{final_label}",
                binary_label=binary_label,
                final_label=final_label,
            )
        )
    return rows


def build_raw_capture_frame(
    root: Path,
    dataset_name: str,
    tshark_path: str,
    seed: int,
    min_packets: int,
    min_bytes: int,
    max_sequence_packets: int,
) -> pd.DataFrame:
    capture_files = iter_capture_files(root)
    rows: list[dict[str, object]] = []
    for index, capture_path in enumerate(capture_files, start=1):
        print(f"[raw] {dataset_name} {index}/{len(capture_files)}: {capture_path.name}")
        rows.extend(
            build_raw_capture_rows(
                capture_path=capture_path,
                dataset_name=dataset_name,
                tshark_path=tshark_path,
                min_packets=min_packets,
                min_bytes=min_bytes,
                max_sequence_packets=max_sequence_packets,
            )
        )

    frame = pd.DataFrame(rows)
    if frame.empty:
        empty = pd.DataFrame(
            columns=[
                "raw_label",
                "binary_label",
                "final_label",
                "transport",
                "sequence_text",
                "split",
            ] + COMMON_NUMERIC_FEATURES
        )
        return finalize_frame(empty, source_name=dataset_name)

    split_label = "final_label" if frame["final_label"].nunique() > 1 else "raw_label"
    frame["split"] = assign_split(frame, label_col=split_label, seed=seed).to_numpy()
    return finalize_frame(frame.drop(columns=["capture_name"], errors="ignore"), source_name=dataset_name)


def map_flow_final_label(label: str) -> str | None:
    normalized = label.strip().upper()
    if normalized in {"TLS", "DTLS"}:
        return "TLS_FAMILY"
    if normalized == "SSH":
        return "SSH"
    if normalized == "QUIC":
        return "QUIC"
    if normalized in {"WIREGUARD", "OPENVPN"}:
        return "VPN"
    return None


def build_flow_all_frame(path: Path) -> pd.DataFrame:
    usecols = [
        "encryption_method",
        "split",
        "transport",
        "sequence_text",
        "duration",
        "packet_count",
        "fwd_packet_count",
        "bwd_packet_count",
        "byte_count",
        "fwd_byte_count",
        "bwd_byte_count",
        "packets_per_second",
        "bytes_per_second",
        "mean_packet_len",
        "std_packet_len",
        "min_packet_len",
        "max_packet_len",
        "mean_iat",
        "std_iat",
        "min_iat",
        "max_iat",
        "direction_packet_ratio",
        "direction_byte_ratio",
        "encrypted_packet_ratio",
    ]
    raw = pd.read_csv(path, usecols=usecols, low_memory=False)
    frame = raw.rename(columns={"encryption_method": "raw_label"}).copy()
    frame["avg_packet_size"] = as_numeric(frame["mean_packet_len"])
    frame["binary_label"] = np.where(
        frame["raw_label"].astype(str).str.upper() == "UNKNOWN_OR_NON_ENCRYPTED",
        "NON_ENCRYPTED",
        "ENCRYPTED",
    )
    frame["final_label"] = None
    return finalize_frame(frame, source_name="FLOW_ALL")


def build_flow_labeled_frame(path: Path) -> pd.DataFrame:
    usecols = [
        "encryption_method",
        "split",
        "transport",
        "sequence_text",
        "duration",
        "packet_count",
        "fwd_packet_count",
        "bwd_packet_count",
        "byte_count",
        "fwd_byte_count",
        "bwd_byte_count",
        "packets_per_second",
        "bytes_per_second",
        "mean_packet_len",
        "std_packet_len",
        "min_packet_len",
        "max_packet_len",
        "mean_iat",
        "std_iat",
        "min_iat",
        "max_iat",
        "direction_packet_ratio",
        "direction_byte_ratio",
        "encrypted_packet_ratio",
    ]
    raw = pd.read_csv(path, usecols=usecols, low_memory=False)
    frame = raw.rename(columns={"encryption_method": "raw_label"}).copy()
    frame["avg_packet_size"] = as_numeric(frame["mean_packet_len"])
    frame["binary_label"] = "ENCRYPTED"
    frame["final_label"] = frame["raw_label"].astype(str).map(map_flow_final_label)
    frame = frame.loc[frame["final_label"].notna()].copy()
    return finalize_frame(frame, source_name="FLOW_LABELED")


def map_dataset_binary_label(label: str) -> str | None:
    normalized = label.strip().upper()
    if normalized in {"HTTPS", "SSH", "VPN"}:
        return "ENCRYPTED"
    if normalized in {"DNS", "FTP"}:
        return "NON_ENCRYPTED"
    return None


def map_dataset_final_label(label: str) -> str | None:
    normalized = label.strip().upper()
    if normalized == "HTTPS":
        return "TLS_FAMILY"
    if normalized == "SSH":
        return "SSH"
    if normalized == "VPN":
        return "VPN"
    if normalized in {"DNS", "FTP"}:
        return "NON_ENCRYPTED"
    return None


def build_dataset_csv_frame(path: Path, seed: int) -> pd.DataFrame:
    usecols = [
        "Protocol",
        "Flow Duration",
        "Total Fwd Packet",
        "Total Bwd packets",
        "Total Length of Fwd Packet",
        "Total Length of Bwd Packet",
        "Flow Bytes/s",
        "Flow Packets/s",
        "Flow IAT Mean",
        "Flow IAT Std",
        "Flow IAT Max",
        "Flow IAT Min",
        "Packet Length Min",
        "Packet Length Max",
        "Packet Length Mean",
        "Packet Length Std",
        "Average Packet Size",
        "Label",
    ]
    raw = pd.read_csv(path, usecols=usecols, low_memory=False)

    fwd_packets = as_numeric(raw["Total Fwd Packet"])
    bwd_packets = as_numeric(raw["Total Bwd packets"])
    fwd_bytes = as_numeric(raw["Total Length of Fwd Packet"])
    bwd_bytes = as_numeric(raw["Total Length of Bwd Packet"])
    labels = raw["Label"].astype(str).str.strip()

    frame = pd.DataFrame(
        {
            "raw_label": labels,
            "transport": raw["Protocol"].map(standardize_transport),
            "duration": as_numeric(raw["Flow Duration"]),
            "packet_count": fwd_packets + bwd_packets,
            "fwd_packet_count": fwd_packets,
            "bwd_packet_count": bwd_packets,
            "byte_count": fwd_bytes + bwd_bytes,
            "fwd_byte_count": fwd_bytes,
            "bwd_byte_count": bwd_bytes,
            "packets_per_second": as_numeric(raw["Flow Packets/s"]),
            "bytes_per_second": as_numeric(raw["Flow Bytes/s"]),
            "mean_packet_len": as_numeric(raw["Packet Length Mean"]),
            "std_packet_len": as_numeric(raw["Packet Length Std"]),
            "min_packet_len": as_numeric(raw["Packet Length Min"]),
            "max_packet_len": as_numeric(raw["Packet Length Max"]),
            "mean_iat": as_numeric(raw["Flow IAT Mean"]),
            "std_iat": as_numeric(raw["Flow IAT Std"]),
            "min_iat": as_numeric(raw["Flow IAT Min"]),
            "max_iat": as_numeric(raw["Flow IAT Max"]),
            "direction_packet_ratio": fwd_packets / (bwd_packets + 1.0),
            "direction_byte_ratio": fwd_bytes / (bwd_bytes + 1.0),
            "avg_packet_size": as_numeric(raw["Average Packet Size"]),
            "encrypted_packet_ratio": np.nan,
            "sequence_text": "",
        }
    )
    frame["binary_label"] = labels.map(map_dataset_binary_label)
    frame["final_label"] = labels.map(map_dataset_final_label)
    frame = frame.loc[frame["binary_label"].notna()].copy()
    frame["split"] = assign_split(frame, label_col="raw_label", seed=seed).to_numpy()
    return finalize_frame(frame, source_name="DATASET_CSV")


def map_bccc_binary_label(label: str) -> str | None:
    normalized = label.strip().upper()
    if normalized == "ENCRYPTED":
        return "ENCRYPTED"
    if normalized == "NON-ENCRYPTED":
        return "NON_ENCRYPTED"
    return None


def map_bccc_binary_final_label(label: str) -> str | None:
    normalized = label.strip().upper()
    if normalized == "NON-ENCRYPTED":
        return "NON_ENCRYPTED"
    return None


def build_bccc_binary_frame(path: Path, seed: int) -> pd.DataFrame:
    usecols = [
        "protocol",
        "duration",
        "packets_count",
        "fwd_packets_count",
        "bwd_packets_count",
        "total_payload_bytes",
        "fwd_total_payload_bytes",
        "bwd_total_payload_bytes",
        "total_header_bytes",
        "fwd_total_header_bytes",
        "bwd_total_header_bytes",
        "bytes_rate",
        "packets_rate",
        "segment_size_mean",
        "segment_size_std",
        "segment_size_min",
        "segment_size_max",
        "packets_IAT_mean",
        "packet_IAT_std",
        "packet_IAT_min",
        "packet_IAT_max",
        "label",
    ]
    raw = pd.read_csv(path, usecols=usecols, low_memory=False)

    fwd_packets = as_numeric(raw["fwd_packets_count"])
    bwd_packets = as_numeric(raw["bwd_packets_count"])
    fwd_bytes = as_numeric(raw["fwd_total_payload_bytes"]) + as_numeric(raw["fwd_total_header_bytes"])
    bwd_bytes = as_numeric(raw["bwd_total_payload_bytes"]) + as_numeric(raw["bwd_total_header_bytes"])
    labels = raw["label"].astype(str).str.strip()

    frame = pd.DataFrame(
        {
            "raw_label": labels,
            "transport": raw["protocol"].map(standardize_transport),
            "duration": as_numeric(raw["duration"]),
            "packet_count": as_numeric(raw["packets_count"]),
            "fwd_packet_count": fwd_packets,
            "bwd_packet_count": bwd_packets,
            "byte_count": fwd_bytes + bwd_bytes,
            "fwd_byte_count": fwd_bytes,
            "bwd_byte_count": bwd_bytes,
            "packets_per_second": as_numeric(raw["packets_rate"]),
            "bytes_per_second": as_numeric(raw["bytes_rate"]),
            "mean_packet_len": as_numeric(raw["segment_size_mean"]),
            "std_packet_len": as_numeric(raw["segment_size_std"]),
            "min_packet_len": as_numeric(raw["segment_size_min"]),
            "max_packet_len": as_numeric(raw["segment_size_max"]),
            "mean_iat": as_numeric(raw["packets_IAT_mean"]),
            "std_iat": as_numeric(raw["packet_IAT_std"]),
            "min_iat": as_numeric(raw["packet_IAT_min"]),
            "max_iat": as_numeric(raw["packet_IAT_max"]),
            "direction_packet_ratio": fwd_packets / (bwd_packets + 1.0),
            "direction_byte_ratio": fwd_bytes / (bwd_bytes + 1.0),
            "avg_packet_size": as_numeric(raw["segment_size_mean"]),
            "encrypted_packet_ratio": np.nan,
            "sequence_text": "",
        }
    )
    frame["binary_label"] = labels.map(map_bccc_binary_label)
    frame["final_label"] = labels.map(map_bccc_binary_final_label)
    frame = frame.loc[frame["binary_label"].notna()].copy()
    frame["split"] = assign_split(frame, label_col="raw_label", seed=seed).to_numpy()
    return finalize_frame(frame, source_name="BCCC_BINARY")


def map_bccc_multi_final_label(label: str) -> str | None:
    normalized = label.strip().upper()
    if normalized in {"VPN", "TOR", "I2P", "FREENET", "ZERONET"}:
        return normalized
    return None


def build_bccc_multiclass_frame(path: Path, seed: int) -> pd.DataFrame:
    usecols = [
        "protocol",
        "duration",
        "packets_count",
        "fwd_packets_count",
        "bwd_packets_count",
        "total_payload_bytes",
        "fwd_total_payload_bytes",
        "bwd_total_payload_bytes",
        "total_header_bytes",
        "fwd_total_header_bytes",
        "bwd_total_header_bytes",
        "bytes_rate",
        "packets_rate",
        "segment_size_mean",
        "segment_size_std",
        "segment_size_min",
        "segment_size_max",
        "packets_IAT_mean",
        "packet_IAT_std",
        "packet_IAT_min",
        "packet_IAT_max",
        "label",
    ]
    raw = pd.read_csv(path, usecols=usecols, low_memory=False)

    fwd_packets = as_numeric(raw["fwd_packets_count"])
    bwd_packets = as_numeric(raw["bwd_packets_count"])
    fwd_bytes = as_numeric(raw["fwd_total_payload_bytes"]) + as_numeric(raw["fwd_total_header_bytes"])
    bwd_bytes = as_numeric(raw["bwd_total_payload_bytes"]) + as_numeric(raw["bwd_total_header_bytes"])
    labels = raw["label"].astype(str).str.strip()

    frame = pd.DataFrame(
        {
            "raw_label": labels,
            "transport": raw["protocol"].map(standardize_transport),
            "duration": as_numeric(raw["duration"]),
            "packet_count": as_numeric(raw["packets_count"]),
            "fwd_packet_count": fwd_packets,
            "bwd_packet_count": bwd_packets,
            "byte_count": fwd_bytes + bwd_bytes,
            "fwd_byte_count": fwd_bytes,
            "bwd_byte_count": bwd_bytes,
            "packets_per_second": as_numeric(raw["packets_rate"]),
            "bytes_per_second": as_numeric(raw["bytes_rate"]),
            "mean_packet_len": as_numeric(raw["segment_size_mean"]),
            "std_packet_len": as_numeric(raw["segment_size_std"]),
            "min_packet_len": as_numeric(raw["segment_size_min"]),
            "max_packet_len": as_numeric(raw["segment_size_max"]),
            "mean_iat": as_numeric(raw["packets_IAT_mean"]),
            "std_iat": as_numeric(raw["packet_IAT_std"]),
            "min_iat": as_numeric(raw["packet_IAT_min"]),
            "max_iat": as_numeric(raw["packet_IAT_max"]),
            "direction_packet_ratio": fwd_packets / (bwd_packets + 1.0),
            "direction_byte_ratio": fwd_bytes / (bwd_bytes + 1.0),
            "avg_packet_size": as_numeric(raw["segment_size_mean"]),
            "encrypted_packet_ratio": np.nan,
            "sequence_text": "",
        }
    )
    frame["binary_label"] = "ENCRYPTED"
    frame["final_label"] = labels.map(map_bccc_multi_final_label)
    frame = frame.loc[frame["final_label"].notna()].copy()
    frame["split"] = assign_split(frame, label_col="raw_label", seed=seed).to_numpy()
    return finalize_frame(frame, source_name="BCCC_MULTI")


def collect_counts(df: pd.DataFrame, label_col: str) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for split_name, group in df.groupby("split"):
        counts = group[label_col].value_counts().sort_index().to_dict()
        result[split_name] = {str(key): int(value) for key, value in counts.items()}
    return result


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_csv_path = Path(args.dataset_csv)
    bccc_binary_path = Path(args.bccc_binary_csv)
    bccc_multiclass_path = Path(args.bccc_multiclass_csv)
    flow_all_path = Path(args.flow_all_csv)
    flow_labeled_path = Path(args.flow_labeled_csv)
    tor_dir = Path(args.tor_dir)
    nontor_dir = Path(args.nontor_dir)

    for path in (
        dataset_csv_path,
        bccc_binary_path,
        bccc_multiclass_path,
        flow_all_path,
        flow_labeled_path,
    ):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")
    for path in (tor_dir, nontor_dir):
        if not path.exists():
            raise FileNotFoundError(f"Required raw capture directory not found: {path}")

    tshark_path = locate_tshark()

    flow_all = build_flow_all_frame(flow_all_path)
    flow_labeled = build_flow_labeled_frame(flow_labeled_path)
    dataset_csv = build_dataset_csv_frame(dataset_csv_path, seed=args.random_state)
    bccc_binary = build_bccc_binary_frame(bccc_binary_path, seed=args.random_state)
    bccc_multiclass = build_bccc_multiclass_frame(bccc_multiclass_path, seed=args.random_state)

    raw_tor = build_raw_capture_frame(
        root=tor_dir,
        dataset_name="RAW_TOR",
        tshark_path=tshark_path,
        seed=args.random_state,
        min_packets=args.raw_min_packets,
        min_bytes=args.raw_min_bytes,
        max_sequence_packets=args.raw_max_seq_packets,
    )
    raw_nontor = build_raw_capture_frame(
        root=nontor_dir,
        dataset_name="RAW_NONTOR",
        tshark_path=tshark_path,
        seed=args.random_state,
        min_packets=args.raw_min_packets,
        min_bytes=args.raw_min_bytes,
        max_sequence_packets=args.raw_max_seq_packets,
    )

    raw_tor.to_csv(output_dir / "raw_tor_flows.csv", index=False)
    raw_nontor.to_csv(output_dir / "raw_nontor_flows.csv", index=False)

    binary_pretrain = pd.concat(
        [
            flow_all.loc[flow_all["binary_label"].notna()],
            dataset_csv.loc[dataset_csv["binary_label"].notna()],
            bccc_binary.loc[bccc_binary["binary_label"].notna()],
            bccc_multiclass.loc[bccc_multiclass["binary_label"].notna()],
            raw_tor.loc[raw_tor["binary_label"].notna()],
            raw_nontor.loc[raw_nontor["binary_label"].notna()],
        ],
        ignore_index=True,
    )
    multiclass_finetune = pd.concat(
        [
            flow_labeled.loc[flow_labeled["final_label"].notna()],
            dataset_csv.loc[dataset_csv["final_label"].notna()],
            bccc_binary.loc[bccc_binary["final_label"].notna()],
            bccc_multiclass.loc[bccc_multiclass["final_label"].notna()],
            raw_tor.loc[raw_tor["final_label"].notna()],
            raw_nontor.loc[raw_nontor["final_label"].notna()],
        ],
        ignore_index=True,
    )

    binary_pretrain["sample_id"] = np.arange(len(binary_pretrain))
    multiclass_finetune["sample_id"] = np.arange(len(multiclass_finetune))

    binary_path = output_dir / "binary_pretrain.csv"
    multiclass_path = output_dir / "multiclass_finetune.csv"
    binary_pretrain.to_csv(binary_path, index=False)
    multiclass_finetune.to_csv(multiclass_path, index=False)

    metadata = {
        "common_numeric_features": COMMON_NUMERIC_FEATURES,
        "binary_label_order": BINARY_LABEL_ORDER,
        "final_label_order": FINAL_LABEL_ORDER,
        "sources": {
            "dataset_csv": str(dataset_csv_path),
            "bccc_binary": str(bccc_binary_path),
            "bccc_multiclass": str(bccc_multiclass_path),
            "flow_all": str(flow_all_path),
            "flow_labeled": str(flow_labeled_path),
            "tor_dir": str(tor_dir),
            "nontor_dir": str(nontor_dir),
            "tshark_path": tshark_path,
        },
        "binary_pretrain": {
            "rows": int(len(binary_pretrain)),
            "counts_by_split": collect_counts(binary_pretrain, "binary_label"),
            "counts_by_source": {
                source: int(count)
                for source, count in binary_pretrain["source_name"].value_counts().sort_index().items()
            },
        },
        "multiclass_finetune": {
            "rows": int(len(multiclass_finetune)),
            "counts_by_split": collect_counts(multiclass_finetune, "final_label"),
            "counts_by_source": {
                source: int(count)
                for source, count in multiclass_finetune["source_name"].value_counts().sort_index().items()
            },
        },
    }
    metadata_path = output_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Unified dataset build complete.")
    print(f"Binary pretrain csv : {binary_path}")
    print(f"Multiclass csv      : {multiclass_path}")
    print(f"Metadata            : {metadata_path}")
    print()
    print("Binary counts by split:")
    for split_name, counts in metadata["binary_pretrain"]["counts_by_split"].items():
        print(f"- {split_name}: {counts}")
    print("Multiclass counts by split:")
    for split_name, counts in metadata["multiclass_finetune"]["counts_by_split"].items():
        print(f"- {split_name}: {counts}")


if __name__ == "__main__":
    main()
