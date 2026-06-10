from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import load_config, project_relative_path
from .live_capture import CaptureSettings, LiveCaptureManager
from .predictor import RoutedModelPredictor
from .schemas import (
    CaptureResultsResponse,
    CaptureStartRequest,
    CaptureStatusResponse,
    CsvPredictionResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
)


config = load_config()
predictor = RoutedModelPredictor(
    primary_model_dir=config.model_dir,
    fallback_model_dir=config.fallback_model_dir,
    data_metadata_path=config.data_metadata_path,
).load()
live_capture = LiveCaptureManager(predictor=predictor, max_results=config.max_live_results)

app = FastAPI(
    title="Encrypted Network Traffic Method Identification System",
    description="Full backend API for the enhanced encryption-method identification model.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def model_info_payload() -> dict:
    metadata = predictor.metadata()
    return {
        "model_name": metadata.model_name,
        "labels": metadata.label_names,
        "numeric_features": metadata.numeric_features,
        "transport_categories": metadata.transport_categories,
        "sequence_features": metadata.sequence_features,
        "metrics": {
            "accuracy": metadata.metrics.get("accuracy"),
            "f1_macro": metadata.metrics.get("f1_macro"),
            "f1_weighted": metadata.metrics.get("f1_weighted"),
            "macro_recall": metadata.metrics.get("macro_recall"),
        },
        "routing": metadata.routing,
    }


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=predictor.loaded, model_dir=project_relative_path(config.model_dir))


@app.get("/api/model/info")
def model_info() -> dict:
    return model_info_payload()


@app.get("/api/admin/summary")
def admin_summary() -> dict:
    return {
        "service": {
            "title": app.title,
            "version": app.version,
            "model_loaded": predictor.loaded,
        },
        "paths": {
            "primary_model_dir": project_relative_path(config.model_dir),
            "fallback_model_dir": project_relative_path(config.fallback_model_dir),
            "data_metadata_path": project_relative_path(config.data_metadata_path),
            "frontend_dir": project_relative_path(config.frontend_dir),
        },
        "limits": {
            "max_batch_records": config.max_batch_records,
            "max_live_results": config.max_live_results,
        },
        "runtime": {
            "tshark_path": config.tshark_path,
        },
        "model": model_info_payload(),
        "capture": live_capture.status(),
    }


@app.get("/api/capture/interfaces")
def capture_interfaces(tshark_path: str | None = Query(None)) -> dict:
    try:
        interfaces = live_capture.list_interfaces(tshark_path or config.tshark_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"interfaces": interfaces}


@app.post("/api/capture/start", response_model=CaptureStatusResponse)
def capture_start(request: CaptureStartRequest) -> CaptureStatusResponse:
    try:
        status = live_capture.start(
            CaptureSettings(
                interface=request.interface,
                tshark_path=request.tshark_path or config.tshark_path,
                capture_filter=request.capture_filter,
                flow_idle_timeout=request.flow_idle_timeout,
                emit_interval=request.emit_interval,
                min_packets=request.min_packets,
                max_sequence_packets=request.max_sequence_packets,
                include_probabilities=request.include_probabilities,
            )
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CaptureStatusResponse(**status)


@app.post("/api/capture/stop", response_model=CaptureStatusResponse)
def capture_stop() -> CaptureStatusResponse:
    return CaptureStatusResponse(**live_capture.stop())


@app.get("/api/capture/status", response_model=CaptureStatusResponse)
def capture_status() -> CaptureStatusResponse:
    return CaptureStatusResponse(**live_capture.status())


@app.get("/api/capture/results", response_model=CaptureResultsResponse)
def capture_results(limit: int = Query(100, ge=1, le=500), since_id: int | None = Query(None)) -> CaptureResultsResponse:
    results = live_capture.results(limit=limit, since_id=since_id)
    return CaptureResultsResponse(count=len(results), results=results)


@app.post("/api/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    if len(request.records) > config.max_batch_records:
        raise HTTPException(status_code=413, detail=f"Too many records. Limit: {config.max_batch_records}")
    try:
        predictions = predictor.predict_records(
            request.records,
            include_probabilities=request.include_probabilities,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PredictionResponse(
        model_name=predictor.model_name,
        labels=predictor.label_names,
        count=len(predictions),
        predictions=predictions,
    )


@app.post("/api/predict/csv", response_model=CsvPredictionResponse)
async def predict_csv(
    request: Request,
    include_probabilities: bool = Query(False),
) -> CsvPredictionResponse:
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="CSV request body is empty.")
    try:
        csv_text = body.decode("utf-8-sig")
        predictions = predictor.predict_csv_text(csv_text, include_probabilities=include_probabilities)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if len(predictions) > config.max_batch_records:
        raise HTTPException(status_code=413, detail=f"Too many records. Limit: {config.max_batch_records}")
    return CsvPredictionResponse(
        model_name=predictor.model_name,
        labels=predictor.label_names,
        count=len(predictions),
        predictions=predictions,
    )


if config.frontend_dir.exists():
    app.mount("/assets", StaticFiles(directory=config.frontend_dir), name="assets")


@app.get("/")
def index() -> FileResponse:
    index_path = config.frontend_dir / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)


@app.get("/admin")
def admin_index() -> FileResponse:
    admin_path = config.frontend_dir / "admin.html"
    if not admin_path.exists():
        raise HTTPException(status_code=404, detail="Frontend admin.html not found.")
    return FileResponse(admin_path)
