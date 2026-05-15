from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    client = TestClient(app)
    for route in [
        "/",
        "/memory-board",
        "/replay",
        "/owners",
        "/docs",
        "/api/dashboard/summary",
        "/api/decisions",
        "/api/timeline",
        "/api/owners",
    ]:
        response = client.get(route)
        response.raise_for_status()
    response = client.post(
        "/api/analyze/recollection",
        json={
            "prompt": "Need retention strategy decision context",
            "freshness_budget_days": 30,
        },
    )
    response.raise_for_status()
    print("smoke-ok")


if __name__ == "__main__":
    main()
