from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable


SOFTWARE_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = SOFTWARE_DIR.parent
AUTO_VALUES = {"", "auto", "detect", "tshark"}


def _path_from_value(value: str | Path) -> Path:
    return Path(os.path.expandvars(str(value))).expanduser()


def _relative_candidates(value: str | Path) -> Iterable[Path]:
    path = _path_from_value(value)
    if path.is_absolute():
        yield path
        return
    yield Path.cwd() / path
    yield PROJECT_ROOT / path
    yield SOFTWARE_DIR / path


def _registry_candidates() -> Iterable[Path]:
    if os.name != "nt":
        return
    try:
        import winreg
    except ImportError:
        return

    app_path_keys = (
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\tshark.exe",
    )
    for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for subkey in app_path_keys:
            try:
                with winreg.OpenKey(root, subkey) as key:
                    value, _ = winreg.QueryValueEx(key, None)
            except OSError:
                continue
            if value:
                yield _path_from_value(value)


def _windows_install_candidates() -> Iterable[Path]:
    if os.name != "nt":
        return
    for env_name in ("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432", "LocalAppData"):
        base = os.getenv(env_name)
        if base:
            yield _path_from_value(base) / "Wireshark" / "tshark.exe"


def tshark_candidates(preferred: str | Path | None = None) -> list[Path]:
    candidates: list[Path] = []

    if preferred and str(preferred).strip().lower() not in AUTO_VALUES:
        candidates.extend(_relative_candidates(preferred))

    for env_name in ("EIM_TSHARK_PATH", "TSHARK_PATH"):
        env_value = os.getenv(env_name)
        if env_value and env_value.strip().lower() not in AUTO_VALUES:
            candidates.extend(_relative_candidates(env_value))

    for local_value in (
        "tools/tshark.exe",
        "tools/tshark",
        "bin/tshark.exe",
        "bin/tshark",
    ):
        candidates.extend(_relative_candidates(local_value))

    found = shutil.which("tshark")
    if found:
        candidates.append(_path_from_value(found))

    candidates.extend(_registry_candidates() or [])
    candidates.extend(_windows_install_candidates() or [])

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).casefold() if os.name == "nt" else str(candidate)
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def find_tshark_path(preferred: str | Path | None = None) -> str | None:
    for candidate in tshark_candidates(preferred):
        if candidate.exists():
            return str(candidate.resolve())
    return None


def resolve_tshark_path(preferred: str | Path | None = None) -> str:
    found = find_tshark_path(preferred)
    if found:
        return found
    requested = str(preferred or "auto")
    raise FileNotFoundError(
        f"tshark not found for '{requested}'. Checked software_system/tools, "
        "EIM_TSHARK_PATH, TSHARK_PATH, PATH, Windows App Paths, and Wireshark install folders."
    )
