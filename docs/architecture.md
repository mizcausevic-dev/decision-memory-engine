# Decision Memory Engine Architecture

## Intent

This repo stores decisions as reusable memory artifacts rather than one-time
conclusions.

The service is designed to answer:

- what was decided
- why it was decided
- what assumptions made it safe
- which signals have gone stale since then
- whether the decision can be reused in a new context

## Flow

1. `app/data/sample_decision_memory.py` stores the seeded decision records.
2. `app/services/decision_memory_service.py` computes owner lanes, replay
   timelines, and recollection scoring.
3. `app/main.py` exposes HTML and API routes for overview, replay, and operator
   inspection.
4. `app/render.py` generates the HTML proof surfaces and static screenshot scenes.
5. `scripts/render_readme_assets.py` captures PNG screenshots from the repo-owned
   HTML scenes.

## Core surfaces

- `/`
  - Overview page
- `/memory-board`
  - Ranked decision memory board
- `/replay`
  - Timeline and recollection scoring proof
- `/owners`
  - Owner-lane pressure view
- `/docs`
  - API summary and sample payload
- `/api/decisions`
  - Full decision list
- `/api/timeline`
  - Replay timeline
- `/api/analyze/recollection`
  - Prompt-based recollection scoring

## Validation

- `py -3.11 -m unittest discover -s tests`
- `py -3.11 scripts\run_demo.py`
- `py -3.11 scripts\smoke_check.py`
- `py -3.11 scripts\render_readme_assets.py`
