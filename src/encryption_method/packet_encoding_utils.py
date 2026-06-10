from __future__ import annotations

import numpy as np
from scapy.all import IP, IPv6, TCP, UDP


def extract_paper_bytes(packet, pad_udp_to_tcp_header: bool = True) -> bytes | None:
    """Extract transport header and payload bytes used by packet-sequence baselines."""
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
        transport_and_payload = transport_and_payload[:8] + (b"\x00" * 12) + transport_and_payload[8:]
    elif TCP not in packet and UDP not in packet:
        return None

    return transport_and_payload


def pad_or_truncate(raw_bytes: bytes, packet_size: int) -> np.ndarray:
    packet_array = np.frombuffer(raw_bytes[:packet_size], dtype=np.uint8)
    if packet_array.size < packet_size:
        packet_array = np.pad(packet_array, (0, packet_size - packet_array.size), mode="constant")
    return packet_array.astype(np.uint8, copy=False)


def _cut(text: str, step: int) -> list[str]:
    result = [text[index : index + step] for index in range(0, len(text), step)]
    try:
        remanent_count = len(result[0]) % 4
    except IndexError:
        return []
    if remanent_count == 0:
        return result
    return [text[index : index + step + remanent_count] for index in range(0, len(text), step + remanent_count)]


def bigram_generation(packet_datagram: str, token_len: int = 64, flag: bool = True) -> str:
    """TrafficFormer-compatible adjacent-byte bigram tokenization."""
    del flag
    result: list[str] = []
    generated_datagram = _cut(packet_datagram, 1)
    for sub_string_index in range(max(len(generated_datagram) - 1, 0)):
        if len(result) >= token_len:
            break
        result.append(generated_datagram[sub_string_index] + generated_datagram[sub_string_index + 1])
    return " ".join(result) + (" " if result else "")
