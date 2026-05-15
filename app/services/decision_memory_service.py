from __future__ import annotations

from collections import Counter
from typing import Any

from app.data.sample_decision_memory import SAMPLE_DATA


class DecisionMemoryService:
    @staticmethod
    def summary() -> dict[str, Any]:
        return SAMPLE_DATA["dashboard"]

    @staticmethod
    def decisions() -> list[dict[str, Any]]:
        severity = {"recover": 0, "watch": 1, "ready": 2}
        return sorted(
            SAMPLE_DATA["decisions"],
            key=lambda decision: (
                severity.get(decision["status"], 9),
                decision["next_review"],
            ),
        )

    @staticmethod
    def decision_by_id(decision_id: str) -> dict[str, Any] | None:
        return next(
            (
                decision
                for decision in SAMPLE_DATA["decisions"]
                if decision["id"] == decision_id
            ),
            None,
        )

    @staticmethod
    def owner_lanes() -> list[dict[str, Any]]:
        lanes = []
        for owner in sorted({decision["owner"] for decision in SAMPLE_DATA["decisions"]}):
            owned = [
                decision for decision in SAMPLE_DATA["decisions"] if decision["owner"] == owner
            ]
            lanes.append(
                {
                    "owner": owner,
                    "decisionCount": len(owned),
                    "watchCount": len(
                        [decision for decision in owned if decision["status"] != "ready"]
                    ),
                    "focusDecision": max(
                        owned,
                        key=lambda decision: (
                            decision["status"] != "ready",
                            len(decision["stale_signals"]),
                        ),
                    )["title"],
                    "domains": sorted({decision["domain"] for decision in owned}),
                }
            )
        return lanes

    @staticmethod
    def timeline() -> list[dict[str, Any]]:
        return [
            {
                "id": decision["id"],
                "title": decision["title"],
                "decidedAt": decision["decided_at"],
                "nextReview": decision["next_review"],
                "status": decision["status"],
                "staleSignalCount": len(decision["stale_signals"]),
            }
            for decision in sorted(
                SAMPLE_DATA["decisions"], key=lambda decision: decision["decided_at"]
            )
        ]

    @staticmethod
    def sample_decision() -> dict[str, Any]:
        return DecisionMemoryService.decisions()[0]

    @staticmethod
    def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
        prompt = str(payload.get("prompt", "")).lower()
        freshness_budget = int(payload.get("freshness_budget_days", 30))
        ranked = []
        domain_hits = Counter()

        for decision in SAMPLE_DATA["decisions"]:
            keyword_hits = sum(
                1
                for token in (
                    decision["domain"].split()
                    + decision["title"].lower().split()
                    + [source.lower() for source in decision["sources"]]
                )
                if token in prompt
            )
            stale_penalty = max(len(decision["stale_signals"]) * 3, 0)
            confidence_bonus = round(float(decision["confidence"]) * 12, 1)
            review_pressure = 4 if freshness_budget < decision["outcome_window_days"] else 0
            score = (keyword_hits * 6) + confidence_bonus - stale_penalty - review_pressure
            ranked.append(
                {
                    "id": decision["id"],
                    "title": decision["title"],
                    "domain": decision["domain"],
                    "status": decision["status"],
                    "score": round(score, 1),
                    "keywordHits": keyword_hits,
                    "staleSignalCount": len(decision["stale_signals"]),
                }
            )
            domain_hits[decision["domain"]] += keyword_hits

        ranked.sort(key=lambda item: (-item["score"], item["staleSignalCount"]))
        top = ranked[0]
        top_decision = DecisionMemoryService.decision_by_id(top["id"])
        posture = "recover"
        if top["score"] >= 18 and top["staleSignalCount"] <= 1:
            posture = "ready"
        elif top["score"] >= 11:
            posture = "watch"

        return {
            "status": posture,
            "topDecision": top,
            "dominantDomain": domain_hits.most_common(1)[0][0] if domain_hits else "unknown",
            "nextAction": {
                "ready": "Reuse the top decision as the anchor context and attach one current operator note before briefing distribution.",
                "watch": "Reuse the decision carefully, but refresh stale assumptions before carrying it into a new operating context.",
                "recover": "Too much decision context has drifted. Reconstruct the rationale chain before treating it as briefing-safe memory.",
            }[posture],
            "staleAssumptions": top_decision["stale_signals"] if top_decision else [],
            "rankedDecisions": ranked,
        }
