from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .tshark_discovery import find_tshark_path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOFTWARE_DIR = PROJECT_ROOT / "software_system"


def resolve_project_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (PROJECT_ROOT / path).resolve()


def project_relative_path(value: str | Path) -> str:
    path = Path(value)
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_env_file(env_path: Path = SOFTWARE_DIR / ".env") -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


@dataclass(frozen=True)
class AppConfig:
    project_root: Path = PROJECT_ROOT
    model_dir: Path = PROJECT_ROOT / "outputs" / "encryption_method" / "full_enhanced_fusion_v1"
    fallback_model_dir: Path = PROJECT_ROOT / "outputs" / "encryption_method" / "broad_fallback_v1"
    data_metadata_path: Path = PROJECT_ROOT / "data" / "unified_encryption_method_v2_all_data" / "metadata.json"
    frontend_dir: Path = PROJECT_ROOT / "software_system" / "frontend"
    tshark_path: str = "auto"
    max_batch_records: int = 20000
    max_live_results: int = 500


def load_config() -> AppConfig:
    load_env_file()
    configured_tshark = os.getenv("EIM_TSHARK_PATH") or os.getenv("TSHARK_PATH") or AppConfig.tshark_path
    discovered_tshark = find_tshark_path(configured_tshark)
    return AppConfig(
        model_dir=resolve_project_path(os.getenv("EIM_MODEL_DIR", project_relative_path(AppConfig.model_dir))),
        fallback_model_dir=resolve_project_path(
            os.getenv("EIM_FALLBACK_MODEL_DIR", project_relative_path(AppConfig.fallback_model_dir))
        ),
        data_metadata_path=resolve_project_path(
            os.getenv("EIM_DATA_METADATA", project_relative_path(AppConfig.data_metadata_path))
        ),
        frontend_dir=resolve_project_path(os.getenv("EIM_FRONTEND_DIR", project_relative_path(AppConfig.frontend_dir))),
        tshark_path=discovered_tshark or configured_tshark,
        max_batch_records=int(os.getenv("EIM_MAX_BATCH_RECORDS", str(AppConfig.max_batch_records))),
        max_live_results=int(os.getenv("EIM_MAX_LIVE_RESULTS", str(AppConfig.max_live_results))),
    )
