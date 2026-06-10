from __future__ import annotations

import json
import math
import subprocess
import threading
import time
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import Any

from .predictor import ModelPredictor
from .tshark_discovery import resolve_tshark_path as discover_tshark_path


LABEL_PRIORITY = ["WIREGUARD", "OPENVPN", "SSH", "QUIC", "DTLS", "TLS"]
UNKNOWN_LABEL = "UNKNOWN_OR_NON_ENCRYPTED"
TSHARK_FIELDS = [
    "frame.time_epoch",
    "frame.len",
    "ip.src",
    "ipv6.src",
    "ip.dst",
    "ipv6.dst",
    "tcp.srcport",
    "tcp.dstport",
    "udp.srcport",
    "udp.dstport",
    "_ws.col.Protocol",
]


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


def canonical_flow_key(src: str, dst: str, sport: str, dport: str, transport: str) -> tuple[str, tuple[str, str], tuple[str, str]]:
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
class LiveFlowStats:
    interface: str
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

    def observed_label(self) -> tuple[str, float]:
        total_encrypted = sum(self.encryption_counts.values())
        if total_encrypted == 0:
            return UNKNOWN_LABEL, 0.0
        best_count = max(self.encryption_counts.values())
        candidates = [label for label, count in self.encryption_counts.items() if count == best_count]
        for label in LABEL_PRIORITY:
            if label in candidates:
                return label, best_count / total_encrypted
        return sorted(candidates)[0], best_count / total_encrypted

    def to_feature_record(self) -> dict[str, Any]:
        duration = max(self.last_time - self.first_time, 0.0)
        mean_len = self.sum_len / self.packet_count if self.packet_count else 0.0
        len_var = max((self.sum_len_sq / self.packet_count) - mean_len * mean_len, 0.0) if self.packet_count else 0.0
        mean_iat = self.iat_sum / self.iat_count if self.iat_count else 0.0
        iat_var = max((self.iat_sum_sq / self.iat_count) - mean_iat * mean_iat, 0.0) if self.iat_count else 0.0
        encrypted_packets = sum(self.encryption_counts.values())

        return {
            "transport": self.transport,
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
            "encrypted_packet_ratio": encrypted_packets / self.packet_count if self.packet_count else 0.0,
            "sequence_text": " ".join(self.sequence_tokens),
        }

    def to_metadata(self) -> dict[str, Any]:
        observed_label, observed_confidence = self.observed_label()
        return {
            "interface": self.interface,
            "flow_key": f"{self.transport}|{self.endpoint_a_ip}:{self.endpoint_a_port}<->{self.endpoint_b_ip}:{self.endpoint_b_port}",
            "endpoint_a_ip": self.endpoint_a_ip,
            "endpoint_a_port": self.endpoint_a_port,
            "endpoint_b_ip": self.endpoint_b_ip,
            "endpoint_b_port": self.endpoint_b_port,
            "first_time": self.first_time,
            "last_time": self.last_time,
            "observed_protocol_label": observed_label,
            "observed_protocol_confidence": observed_confidence,
            "protocol_counts": dict(sorted(self.protocol_counts.items())),
            "encryption_counts": dict(sorted(self.encryption_counts.items())),
        }


@dataclass
class CaptureSettings:
    interface: str
    tshark_path: str = "auto"
    capture_filter: str = "tcp or udp"
    flow_idle_timeout: float = 5.0
    emit_interval: float = 1.0
    min_packets: int = 3
    max_sequence_packets: int = 16
    include_probabilities: bool = False


class LiveCaptureManager:
    def __init__(self, predictor: ModelPredictor, max_results: int = 500) -> None:
        self.predictor = predictor
        self.max_results = max_results
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._process: subprocess.Popen | None = None
        self._reader_thread: threading.Thread | None = None
        self._maintenance_thread: threading.Thread | None = None
        self._flows: dict[tuple[str, tuple[str, str], tuple[str, str]], LiveFlowStats] = {}
        self._results: deque[dict[str, Any]] = deque(maxlen=max_results)
        self._settings: CaptureSettings | None = None
        self._started_at: float | None = None
        self._last_error: str | None = None
        self._packets_seen = 0
        self._packets_skipped = 0
        self._result_id = 0

    def list_interfaces(self, tshark_path: str = "auto") -> list[dict[str, str]]:
        resolved = self.resolve_tshark_path(tshark_path)
        process = subprocess.run(
            [resolved, "-D"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(process.stderr.strip() or "tshark -D failed")
        interfaces: list[dict[str, str]] = []
        for line in process.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            number, _, rest = line.partition(".")
            if not number.isdigit() or not rest:
                interfaces.append({"id": line, "name": line, "raw": line})
                continue
            interfaces.append({"id": number, "name": rest.strip(), "raw": line})
        return interfaces

    def resolve_tshark_path(self, tshark_path: str) -> str:
        return discover_tshark_path(tshark_path)

    def start(self, settings: CaptureSettings) -> dict[str, Any]:
        with self._lock:
            if self.running:
                raise RuntimeError("Live capture is already running.")
            tshark_path = self.resolve_tshark_path(settings.tshark_path)
            self._settings = CaptureSettings(**{**settings.__dict__, "tshark_path": tshark_path})
            self._stop_event.clear()
            self._flows.clear()
            self._results.clear()
            self._started_at = time.time()
            self._last_error = None
            self._packets_seen = 0
            self._packets_skipped = 0
            self._result_id = 0
            command = self._build_tshark_command(self._settings)
            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            self._reader_thread = threading.Thread(target=self._reader_loop, name="live-tshark-reader", daemon=True)
            self._maintenance_thread = threading.Thread(target=self._maintenance_loop, name="live-flow-maintenance", daemon=True)
            self._reader_thread.start()
            self._maintenance_thread.start()
            return self.status()

    def stop(self) -> dict[str, Any]:
        with self._lock:
            if not self.running:
                return self.status()
            self._stop_event.set()
            process = self._process
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        self._flush_all()
        with self._lock:
            self._process = None
            self._settings = None
        return self.status()

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.poll() is None and not self._stop_event.is_set()

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "running": self.running,
                "interface": self._settings.interface if self._settings else None,
                "started_at": self._started_at,
                "uptime_seconds": (time.time() - self._started_at) if self._started_at else 0.0,
                "active_flows": len(self._flows),
                "results_total": self._result_id,
                "packets_seen": self._packets_seen,
                "packets_skipped": self._packets_skipped,
                "last_error": self._last_error,
            }

    def results(self, limit: int = 100, since_id: int | None = None) -> list[dict[str, Any]]:
        with self._lock:
            rows = list(self._results)
        if since_id is not None:
            rows = [row for row in rows if int(row["id"]) > since_id]
        return rows[-limit:]

    def _build_tshark_command(self, settings: CaptureSettings) -> list[str]:
        command = [
            settings.tshark_path,
            "-l",
            "-i",
            settings.interface,
        ]
        if settings.capture_filter.strip():
            command.extend(["-f", settings.capture_filter.strip()])
        command.extend(["-T", "fields", "-E", "separator=\t"])
        for field_name in TSHARK_FIELDS:
            command.extend(["-e", field_name])
        return command

    def _reader_loop(self) -> None:
        assert self._process is not None
        assert self._settings is not None
        stdout = self._process.stdout
        if stdout is None:
            self._last_error = "tshark stdout is not available."
            return
        try:
            for raw_line in stdout:
                if self._stop_event.is_set():
                    break
                self._process_line(raw_line.rstrip("\n"), self._settings)
        except Exception as exc:
            with self._lock:
                self._last_error = str(exc)
        finally:
            self._collect_stderr_if_failed()

    def _maintenance_loop(self) -> None:
        while not self._stop_event.is_set():
            with self._lock:
                settings = self._settings
            if settings is None:
                break
            time.sleep(max(settings.emit_interval, 0.2))
            self._emit_idle_flows(time.time())

    def _process_line(self, line: str, settings: CaptureSettings) -> None:
        fields = line.split("\t")
        if len(fields) < len(TSHARK_FIELDS):
            fields.extend([""] * (len(TSHARK_FIELDS) - len(fields)))
        timestamp = to_float(fields[0], default=time.time())
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
            with self._lock:
                self._packets_skipped += 1
            return

        if not src or not dst or not sport or not dport:
            with self._lock:
                self._packets_skipped += 1
            return

        key = canonical_flow_key(src, dst, sport, dport, transport)
        with self._lock:
            self._packets_seen += 1
            flow = self._flows.get(key)
            if flow is None:
                _, endpoint_a, endpoint_b = key
                flow = LiveFlowStats(
                    interface=settings.interface,
                    transport=transport,
                    endpoint_a_ip=endpoint_a[0],
                    endpoint_a_port=endpoint_a[1],
                    endpoint_b_ip=endpoint_b[0],
                    endpoint_b_port=endpoint_b[1],
                    first_time=timestamp,
                    last_time=timestamp,
                )
                self._flows[key] = flow
            flow.update(
                timestamp=timestamp,
                length=length,
                protocol=protocol,
                encryption_label=normalize_protocol(protocol),
                src=src,
                sport=sport,
                max_sequence_packets=settings.max_sequence_packets,
            )
        self._emit_idle_flows(timestamp)

    def _emit_idle_flows(self, reference_time: float) -> None:
        with self._lock:
            settings = self._settings
            if settings is None:
                return
            due_keys = [
                key
                for key, flow in self._flows.items()
                if flow.packet_count >= settings.min_packets and reference_time - flow.last_time >= settings.flow_idle_timeout
            ]
            flows = [self._flows.pop(key) for key in due_keys]
        for flow in flows:
            self._emit_flow(flow, settings)

    def _flush_all(self) -> None:
        with self._lock:
            settings = self._settings
            if settings is None:
                return
            flows = list(self._flows.values())
            self._flows.clear()
        for flow in flows:
            if flow.packet_count >= settings.min_packets:
                self._emit_flow(flow, settings)

    def _emit_flow(self, flow: LiveFlowStats, settings: CaptureSettings) -> None:
        feature_record = flow.to_feature_record()
        try:
            prediction = self.predictor.predict_records(
                [feature_record],
                include_probabilities=settings.include_probabilities,
            )[0]
        except Exception as exc:
            with self._lock:
                self._last_error = f"Prediction failed: {exc}"
            return
        metadata = flow.to_metadata()
        with self._lock:
            self._result_id += 1
            result = {
                "id": self._result_id,
                "created_at": time.time(),
                **metadata,
                **feature_record,
                "predicted_label": prediction["predicted_label"],
                "confidence": prediction["confidence"],
                "model_used": prediction.get("model_used"),
                "input_profile": prediction.get("input_profile"),
                "missing_numeric_features": prediction.get("missing_numeric_features", []),
            }
            if settings.include_probabilities:
                result["probabilities"] = prediction.get("probabilities", {})
            self._results.append(result)

    def _collect_stderr_if_failed(self) -> None:
        process = self._process
        if process is None:
            return
        returncode = process.poll()
        if returncode is None or returncode == 0 or process.stderr is None:
            return
        try:
            stderr = process.stderr.read().strip()
        except Exception:
            stderr = ""
        if stderr:
            with self._lock:
                self._last_error = stderr[-1000:]


def pretty_command_hint() -> str:
    return "Run `tshark -D` to list interfaces, then use the numeric id or full interface name."
