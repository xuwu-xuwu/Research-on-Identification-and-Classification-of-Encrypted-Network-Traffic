from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    records: list[dict[str, Any]] = Field(..., min_length=1)
    include_probabilities: bool = False


class PredictionItem(BaseModel):
    index: int
    predicted_label: str
    confidence: float
    model_used: str | None = None
    input_profile: str | None = None
    missing_numeric_features: list[str] | None = None
    probabilities: dict[str, float] | None = None


class PredictionResponse(BaseModel):
    model_name: str
    labels: list[str]
    count: int
    predictions: list[PredictionItem]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_dir: str


class CsvPredictionResponse(BaseModel):
    model_name: str
    labels: list[str]
    count: int
    predictions: list[dict[str, Any]]


class CaptureStartRequest(BaseModel):
    interface: str = Field(..., min_length=1)
    tshark_path: str | None = None
    capture_filter: str = "tcp or udp"
    flow_idle_timeout: float = Field(5.0, ge=1.0, le=120.0)
    emit_interval: float = Field(1.0, ge=0.2, le=30.0)
    min_packets: int = Field(3, ge=1, le=1000)
    max_sequence_packets: int = Field(16, ge=1, le=256)
    include_probabilities: bool = False


class CaptureStatusResponse(BaseModel):
    running: bool
    interface: str | None
    started_at: float | None
    uptime_seconds: float
    active_flows: int
    results_total: int
    packets_seen: int
    packets_skipped: int
    last_error: str | None


class CaptureResultsResponse(BaseModel):
    count: int
    results: list[dict[str, Any]]
