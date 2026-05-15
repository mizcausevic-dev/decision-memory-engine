from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.decision_memory_service import DecisionMemoryService


def main() -> None:
    payload = {
        "dashboard": DecisionMemoryService.summary(),
        "topDecision": DecisionMemoryService.sample_decision(),
        "recollection": DecisionMemoryService.evaluate(
            {
                "prompt": "Need board review context for the analytics migration and release gate decision",
                "freshness_budget_days": 30,
            }
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
