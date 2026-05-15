# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-05-15

### Released
- Published **decision-memory-engine** as a FastAPI decision-intelligence artifact focused on rationale recovery, stale assumptions, and context-safe reuse.
- Added owner lanes, replay views, recollection scoring, proof screenshots, tests, and docs.

### Why this mattered
- Teams often reuse prior decisions without recovering the assumptions behind them.
- Decision memory becomes much more useful when it shows expiry pressure, source context, and review windows.

## [0.1.0] - 2026-02-19

### Shipped
- Locked the first internal model for ranking reusable decisions against a fresh prompt and a review horizon.
- Added stale-assumption tracking so reused decisions could be graded instead of copied blindly.

## [Prototype] - 2025-07-08

### Built
- Built the earliest prototype around storing decision rationale and confidence alongside next-review dates.
- Tested whether operator teams could recover useful context faster from structured decision records than from notes alone.

## [Design Phase] - 2024-11-14

### Designed
- Chose a decision-memory framing instead of another meeting-notes or ticket-history tool.
- Treated assumptions and replay context as first-class outputs, not hidden metadata.

## [Idea Origin] - 2023-05-11

### Observed
- High-stakes teams often repeated old decisions because the conclusion was easier to find than the reasoning.
- The missing artifact was a system that could tell operators whether an old decision was still safe to reuse.
