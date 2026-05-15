from __future__ import annotations

SAMPLE_DATA = {
    "catalog": {
        "name": "Northstar Decision Memory Engine",
        "owner": "Kinetic Gain Strategy Systems",
        "publication_url": "http://127.0.0.1:5006",
    },
    "dashboard": {
        "decisionCount": 5,
        "watchDecisions": 2,
        "staleAssumptionLanes": 3,
        "ownerCount": 5,
        "avgConfidence": 0.82,
        "leadRecommendation": (
            "Revisit the decisions carrying stale assumptions before the next "
            "board, launch, or go-to-market briefing inherits outdated logic."
        ),
    },
    "decisions": [
        {
            "id": "dec-101",
            "title": "Prioritize enterprise retention over new-market expansion",
            "domain": "revenue strategy",
            "owner": "Revenue Operations",
            "decided_at": "2026-04-11",
            "confidence": 0.88,
            "status": "watch",
            "outcome_window_days": 90,
            "decision_type": "portfolio allocation",
            "rationale": (
                "Churn volatility and expansion efficiency both indicated higher "
                "short-term leverage in protecting the installed base."
            ),
            "assumptions": [
                "renewal pipeline remains forecastable",
                "support staffing stays above current baseline",
                "pricing pressure does not accelerate in mid-market"
            ],
            "stale_signals": [
                "renewal model refreshed 19 days ago",
                "competitor discounting changed after decision date"
            ],
            "sources": [
                "Q2 retention review",
                "CFO forecast sync",
                "support escalation ledger"
            ],
            "next_review": "2026-05-24",
        },
        {
            "id": "dec-102",
            "title": "Keep the fraud review queue under manual approval for LATAM",
            "domain": "risk operations",
            "owner": "Fraud Systems",
            "decided_at": "2026-04-28",
            "confidence": 0.93,
            "status": "ready",
            "outcome_window_days": 30,
            "decision_type": "risk containment",
            "rationale": (
                "Baggage propagation and dispute trends both showed unstable "
                "signal quality in automated approval lanes."
            ),
            "assumptions": [
                "fraud rule throughput remains within current staffing range",
                "manual-review latency stays under SLA"
            ],
            "stale_signals": [],
            "sources": [
                "fraud signal tracer",
                "dispute latency review",
                "regional payments board"
            ],
            "next_review": "2026-05-19",
        },
        {
            "id": "dec-103",
            "title": "Delay general release of the analytics migration until lineage parity",
            "domain": "platform reliability",
            "owner": "Analytics Platform",
            "decided_at": "2026-03-30",
            "confidence": 0.79,
            "status": "watch",
            "outcome_window_days": 45,
            "decision_type": "release gate",
            "rationale": (
                "Lineage mismatches and incomplete semantic contracts risked "
                "executive reporting drift immediately after cutover."
            ),
            "assumptions": [
                "lineage gaps close in the next sprint",
                "dashboard owners hold publication freeze"
            ],
            "stale_signals": [
                "cutover estimate has moved twice",
                "warehouse freshness improved after the last review"
            ],
            "sources": [
                "semantic metrics catalog",
                "dbt governance review",
                "release readiness gatekeeper"
            ],
            "next_review": "2026-05-18",
        },
        {
            "id": "dec-104",
            "title": "Use showing-intent score to drive same-day follow-up cadence",
            "domain": "real estate operations",
            "owner": "Brokerage Performance",
            "decided_at": "2026-05-03",
            "confidence": 0.77,
            "status": "ready",
            "outcome_window_days": 21,
            "decision_type": "workflow optimization",
            "rationale": (
                "Open-house attendance, listing-match fit, and response-time "
                "history all supported a faster same-day outreach lane."
            ),
            "assumptions": [
                "showing notes remain structured",
                "agent response capacity is balanced by territory"
            ],
            "stale_signals": [],
            "sources": [
                "showing follow-up orchestrator",
                "lead routing command center"
            ],
            "next_review": "2026-05-20",
        },
        {
            "id": "dec-105",
            "title": "Route student re-engagement outreach through advisor-first sequence",
            "domain": "education operations",
            "owner": "Student Success Systems",
            "decided_at": "2026-04-06",
            "confidence": 0.74,
            "status": "recover",
            "outcome_window_days": 60,
            "decision_type": "intervention sequencing",
            "rationale": (
                "Advisor context quality historically outperformed generic "
                "campaign touches for at-risk learners."
            ),
            "assumptions": [
                "advisor notes stay current",
                "curriculum bottlenecks remain unchanged",
                "SMS channel continues to deliver"
            ],
            "stale_signals": [
                "attendance model changed after the decision",
                "advisor staffing ratios deteriorated",
                "support channel mix shifted toward email"
            ],
            "sources": [
                "student success signal hub",
                "advisor outreach orchestrator",
                "learner intervention ledger"
            ],
            "next_review": "2026-05-17",
        },
    ],
}
