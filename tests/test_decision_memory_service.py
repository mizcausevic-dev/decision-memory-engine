from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.decision_memory_service import DecisionMemoryService


class DecisionMemoryEngineTests(unittest.TestCase):
    def test_summary_counts(self) -> None:
        summary = DecisionMemoryService.summary()
        self.assertEqual(summary["decisionCount"], 5)
        self.assertEqual(summary["ownerCount"], 5)

    def test_recollection_returns_ranked_decisions(self) -> None:
        result = DecisionMemoryService.evaluate(
            {
                "prompt": "Need retention strategy context for board review",
                "freshness_budget_days": 30,
            }
        )
        self.assertIn(result["status"], {"ready", "watch", "recover"})
        self.assertGreaterEqual(len(result["rankedDecisions"]), 1)

    def test_api_routes(self) -> None:
        client = TestClient(app)
        response = client.get("/api/decisions/dec-101")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["owner"], "Revenue Operations")


if __name__ == "__main__":
    unittest.main()
