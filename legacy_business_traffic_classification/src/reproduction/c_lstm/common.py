from __future__ import annotations

try:
    import zipfile_inflate64  # type: ignore[import-not-found]
except ImportError:
    zipfile_inflate64 = None

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Iterator
import shutil
import zipfile

import numpy as np
from scapy.all import IP, IPv6, TCP, UDP
from scapy.utils import PcapNgReader, PcapReader


PAPER_LABEL_ORDER = [
    "Chat",
    "Email",
    "File Transfer",
    "P2P",
    "Streaming",
    "VoIP",
    "VPN-Chat",
    "VPN-Email",
    "VPN-File Transfer",
    "VPN-P2P",
    "VPN-Streaming",
    "VPN-VoIP",
]

LABEL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("VPN-Email", ("vpn_email", "vpn_mail")),
    ("VPN-Chat", ("vpn_chat", "vpn_aim", "vpn_icq", "vpn_facebookchat", "vpn_skype_chat")),
    (
        "VPN-File Transfer",
        ("vpn_ftps", "vpn_sftp", "vpn_scp", "vpn_skype_files", "vpn_file"),
    ),
    ("VPN-P2P", ("vpn_bittorrent", "vpn_utorrent", "vpn_transmission", "vpn_torrent", "vpn_p2p")),
    ("VPN-Streaming", ("vpn_netflix", "vpn_vimeo", "vpn_youtube", "vpn_spotify", "vpn_video")),
    ("VPN-VoIP", ("vpn_voipbuster", "vpn_skype_audio", "vpn_hangouts_audio", "vpn_audio", "vpn_voip")),
    ("Email", ("email", "mail")),
    ("Chat", ("facebookchat", "chat", "aim", "icq")),
    ("File Transfer", ("ftps", "sftp", "scp", "ftp", "skype_file", "file")),
    ("P2P", ("bittorrent", "utorrent", "transmission", "torrent", "p2p")),
    ("Streaming", ("netflix", "vimeo", "youtube", "spotify", "video")),
    ("VoIP", ("voipbuster", "hangouts_audio", "audio", "voip")),
]

CAPTURE_EXTENSIONS = {".pcap", ".pcapng"}


@dataclass(frozen=True)
class CaptureEntry:
    display_name: str
    label: str
    source_path: Path
    file_path: Path | None = None
    archive_member: str | None = None


def infer_label(name: str) -> str | None:
    lowered = name.lower()
    for label, patterns in LABEL_RULES:
        if any(pattern in lowered for pattern in patterns):
            return label
    return None


def ordered_labels(labels: Iterable[str]) -> list[str]:
    seen = set(labels)
    ordered = [label for label in PAPER_LABEL_ORDER if label in seen]
    ordered.extend(sorted(seen - set(ordered)))
    return ordered


def iter_capture_entries(sources: Iterable[Path], include_labels: set[str] | None = None) -> Iterator[CaptureEntry]:
    for source in sources:
        if source.is_dir():
            for file_path in sorted(source.rglob("*")):
                if not file_path.is_file() or file_path.suffix.lower() not in CAPTURE_EXTENSIONS:
                    continue
                label = infer_label(file_path.name)
                if label is None or (include_labels and label not in include_labels):
                    continue
                yield CaptureEntry(
                    display_name=str(file_path.relative_to(source)),
                    label=label,
                    source_path=source,
                    file_path=file_path,
                )
            continue

        if source.is_file() and source.suffix.lower() == ".zip":
            with zipfile.ZipFile(source) as archive:
                for member in sorted(archive.namelist()):
                    member_path = Path(member)
                    if member.endswith("/") or member_path.suffix.lower() not in CAPTURE_EXTENSIONS:
                        continue
                    label = infer_label(member_path.name)
                    if label is None or (include_labels and label not in include_labels):
                        continue
                    yield CaptureEntry(
                        display_name=f"{source.name}:{member_path.name}",
                        label=label,
                        source_path=source,
                        archive_member=member,
                    )
            continue

        raise FileNotFoundError(f"Unsupported capture source: {source}")


@contextmanager
def materialize_capture(entry: CaptureEntry) -> Iterator[Path]:
    if entry.file_path is not None:
        yield entry.file_path
        return

    if entry.archive_member is None:
        raise ValueError(f"Archive member is missing for {entry.display_name}")

    temp_root = Path.cwd() / "outputs" / ".tmp_c_lstm"
    temp_root.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="c_lstm_capture_", dir=temp_root) as temp_dir:
        member_name = Path(entry.archive_member).name
        extracted_path = Path(temp_dir) / member_name
        with zipfile.ZipFile(entry.source_path) as archive:
            with archive.open(entry.archive_member) as source_handle, extracted_path.open("wb") as target_handle:
                shutil.copyfileobj(source_handle, target_handle)
        yield extracted_path


def iter_packets(capture_path: Path) -> Iterator:
    reader_cls = PcapNgReader if capture_path.suffix.lower() == ".pcapng" else PcapReader
    reader = reader_cls(str(capture_path))
    try:
        for packet in reader:
            yield packet
    finally:
        reader.close()


def extract_paper_bytes(packet, pad_udp_to_tcp_header: bool = True) -> bytes | None:
    if IP in packet:
        transport_and_payload = bytes(packet[IP].payload)
    elif IPv6 in packet:
        transport_and_payload = bytes(packet[IPv6].payload)
    else:
        return None

    if not transport_and_payload:
        return None

    if UDP in packet and pad_udp_to_tcp_header:
        if len(transport_and_payload) < 8:
            return None
        transport_and_payload = (
            transport_and_payload[:8] + (b"\x00" * 12) + transport_and_payload[8:]
        )
    elif TCP not in packet and UDP not in packet:
        return None

    return transport_and_payload


def pad_or_truncate(raw_bytes: bytes, packet_size: int) -> np.ndarray:
    packet_array = np.frombuffer(raw_bytes[:packet_size], dtype=np.uint8)
    if packet_array.size < packet_size:
        packet_array = np.pad(packet_array, (0, packet_size - packet_array.size), mode="constant")
    return packet_array.astype(np.uint8, copy=False)




