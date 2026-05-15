from __future__ import annotations

import json
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import (
    render_docs,
    render_memory_board,
    render_overview,
    render_owners,
    render_replay,
)
from app.services.decision_memory_service import DecisionMemoryService

app = FastAPI(
    title="Decision Memory Engine",
    version="0.1.0",
    description=(
        "Decision-intelligence service for storing prior decisions, rationale, "
        "confidence, stale assumptions, and operator context recovery."
    ),
)


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/memory-board", response_class=HTMLResponse)
def memory_board() -> str:
    return render_memory_board()


@app.get("/replay", response_class=HTMLResponse)
def replay() -> str:
    return render_replay()


@app.get("/owners", response_class=HTMLResponse)
def owners() -> str:
    return render_owners()


@app.get("/docs", response_class=HTMLResponse)
def docs() -> str:
    return render_docs()


@app.get("/api/dashboard/summary")
def api_summary() -> dict:
    return DecisionMemoryService.summary()


@app.get("/api/decisions")
def api_decisions() -> list[dict]:
    return DecisionMemoryService.decisions()


@app.get("/api/decisions/{decision_id}")
def api_decision(decision_id: str) -> dict:
    decision = DecisionMemoryService.decision_by_id(decision_id)
    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@app.get("/api/timeline")
def api_timeline() -> list[dict]:
    return DecisionMemoryService.timeline()


@app.get("/api/owners")
def api_owners() -> list[dict]:
    return DecisionMemoryService.owner_lanes()


@app.get("/api/sample")
def api_sample() -> dict:
    return DecisionMemoryService.sample_decision()


@app.post("/api/analyze/recollection")
def api_recollection(payload: dict) -> dict:
    return DecisionMemoryService.evaluate(payload)


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5006"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
