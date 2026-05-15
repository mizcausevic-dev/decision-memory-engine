from __future__ import annotations

from html import escape
from pathlib import Path

from app.services.decision_memory_service import DecisionMemoryService


def badge(label: str, tone: str) -> str:
    return f'<span class="badge {tone}">{escape(label)}</span>'


def shell(title: str, subtitle: str, current: str, body: str) -> str:
    summary = DecisionMemoryService.summary()
    nav = [
        ("/", "Overview", "overview"),
        ("/memory-board", "Memory Board", "memory-board"),
        ("/replay", "Replay", "replay"),
        ("/owners", "Owners", "owners"),
        ("/docs", "Docs", "docs"),
    ]
    nav_links = "".join(
        f'<a class="nav-link {"active" if key == current else ""}" href="{href}">{label}</a>'
        for href, label, key in nav
    )
    top_tabs = "".join(
        f'<a class="tab {"active" if key == current else ""}" href="{href}">{label}</a>'
        for href, label, key in nav
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)}</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #05101b;
        --panel: #0b1623;
        --panel-2: #102032;
        --line: rgba(255,255,255,0.08);
        --text: #eef5ff;
        --muted: #9fb3cd;
        --blue: #7ccfff;
        --amber: #f3c36e;
        --green: #63d9a6;
        --red: #ff8796;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Inter, "Segoe UI", system-ui, sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top left, rgba(124,207,255,0.14), transparent 25%),
          linear-gradient(180deg, #02060c 0%, var(--bg) 100%);
      }}
      a {{ color: inherit; text-decoration: none; }}
      .shell {{ min-height: 100vh; display: grid; grid-template-columns: 250px minmax(0,1fr); }}
      .sidebar {{
        border-right: 1px solid rgba(255,255,255,0.06);
        background: rgba(0,0,0,0.28);
        padding: 24px 18px;
        display: flex; flex-direction: column;
      }}
      .brand {{
        display: flex; gap: 14px; align-items: center; padding: 10px 12px 18px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
      }}
      .mark {{
        width: 42px; height: 42px; display: grid; place-items: center; border-radius: 12px;
        background: linear-gradient(135deg, #1090bf, #5e7dff); font-weight: 900;
        box-shadow: 0 0 22px rgba(94,125,255,0.28);
      }}
      .brand strong {{ display:block; font-size:14px; }}
      .brand span {{ display:block; margin-top:4px; color:var(--blue); font-size:10px; letter-spacing:.18em; text-transform:uppercase; }}
      .nav {{
        margin-top: 18px;
      }}
      .nav-link {{
        display:block; padding: 13px 14px; border-radius: 14px; color:#8598b7;
        font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:.12em;
      }}
      .nav-link.active {{ color: var(--blue); background: rgba(124,207,255,0.08); border: 1px solid rgba(124,207,255,0.14); }}
      .nav-link:hover {{ color: var(--text); background: rgba(255,255,255,0.03); }}
      .sidecard {{
        margin-top: auto; border-top: 1px solid rgba(255,255,255,0.06); padding: 18px 12px 6px;
      }}
      .sidecard .k {{ color:#6d809c; font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
      .sidecard .v {{ margin-top:6px; font-size:12px; font-weight:800; }}
      .main {{ padding: 0 32px 32px; }}
      .topbar {{
        position: sticky; top: 0; z-index: 2; display:flex; justify-content:space-between; gap:18px; align-items:center;
        padding: 22px 0 18px; border-bottom: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(5,16,27,0.94), rgba(5,16,27,0.82));
        backdrop-filter: blur(16px);
      }}
      .status {{
        display:inline-flex; gap:10px; align-items:center; padding:10px 14px; border-radius:999px;
        border:1px solid rgba(124,207,255,0.14); background: rgba(124,207,255,0.06);
        color:#d9ebff; font-size:11px; font-weight:800; letter-spacing:.16em; text-transform:uppercase;
      }}
      .dot {{ width:8px; height:8px; border-radius:999px; background:var(--blue); box-shadow: 0 0 12px rgba(124,207,255,0.9); }}
      .meta-row {{ display:flex; gap:16px; }}
      .meta-box {{
        padding:10px 14px; border-radius:16px; border:1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
      }}
      .meta-box span {{ display:block; color:#7084a0; font-size:9px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
      .meta-box strong {{ display:block; margin-top:6px; font-size:12px; font-weight:800; }}
      .hero {{
        margin-top: 28px; border-radius: 30px; border:1px solid var(--line);
        background: linear-gradient(180deg, rgba(10,20,33,0.96), rgba(7,13,22,0.96));
        box-shadow: 0 26px 56px rgba(0,0,0,0.28);
        overflow: hidden;
      }}
      .hero-grid {{ display:grid; grid-template-columns: minmax(0, 1.3fr) 340px; }}
      .hero-copy {{ padding: 30px; }}
      .eyebrow {{ color: var(--blue); font-size: 11px; font-weight: 900; letter-spacing: .26em; text-transform: uppercase; }}
      h1 {{ margin:16px 0 0; font-size: clamp(42px,5vw,72px); line-height:.92; font-family: Georgia, "Times New Roman", serif; letter-spacing:-.05em; }}
      .hero-copy p {{ margin:14px 0 0; color: var(--muted); font-size: 18px; line-height: 1.58; max-width: 780px; }}
      .tabs {{ display:flex; flex-wrap:wrap; gap:10px; margin-top: 20px; }}
      .tab {{
        padding:10px 14px; border-radius:999px; border:1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03); color:#b4c4dc; font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.12em;
      }}
      .tab.active {{ color: var(--amber); border-color: rgba(243,195,110,0.18); background: rgba(243,195,110,0.08); }}
      .hero-kpis {{
        display:grid; grid-template-columns: repeat(5, minmax(0,1fr)); border-top:1px solid rgba(255,255,255,0.06);
      }}
      .hero-kpi {{ padding:18px 20px 20px; border-right:1px solid rgba(255,255,255,0.06); }}
      .hero-kpi:last-child {{ border-right:0; }}
      .label, .kicker {{
        color:#6f83a0; font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase;
      }}
      .hero-kpi .value {{ margin-top:8px; font-size:34px; font-weight:900; }}
      .hero-callout {{
        border-left:1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.02); padding: 28px;
      }}
      .hero-callout h3 {{ margin:0; font-size:12px; font-weight:900; letter-spacing:.16em; text-transform:uppercase; color:#7c90ab; }}
      .hero-callout p {{ margin:14px 0 0; color:#dde8fb; font-size:15px; line-height:1.62; }}
      .section {{
        margin-top: 24px; border-radius: 26px; border:1px solid var(--line); background: var(--panel);
        overflow:hidden; box-shadow: 0 18px 44px rgba(0,0,0,0.22);
      }}
      .section-head {{ padding:22px 24px 16px; border-bottom:1px solid rgba(255,255,255,0.05); }}
      .section-head h2 {{ margin:10px 0 0; font-size:26px; font-family: Georgia, "Times New Roman", serif; letter-spacing:-.03em; }}
      .section-head p {{ margin:10px 0 0; color:var(--muted); font-size:15px; line-height:1.56; max-width:920px; }}
      .section-body {{ padding:24px; }}
      .grid-4, .grid-3, .grid-2 {{ display:grid; gap:18px; }}
      .grid-4 {{ grid-template-columns: repeat(4, minmax(0,1fr)); }}
      .grid-3 {{ grid-template-columns: repeat(3, minmax(0,1fr)); }}
      .grid-2 {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
      .card, .panel {{
        border-radius:20px; border:1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(0,0,0,0.08));
        padding:18px;
      }}
      .card .value {{ margin-top:10px; font-size:36px; font-weight:900; }}
      .card p, .panel p {{ margin:10px 0 0; color:var(--muted); font-size:14px; line-height:1.48; }}
      .decision-card {{
        border-radius:22px; border:1px solid rgba(255,255,255,0.06); background: rgba(4,9,17,0.58); overflow:hidden;
      }}
      .decision-top {{ padding:20px 22px; display:grid; grid-template-columns:minmax(0,1fr) auto; gap:18px; align-items:start; }}
      .decision-top h3 {{ margin:0; font-size:23px; letter-spacing:-.03em; }}
      .meta {{ margin-top:8px; color:var(--muted); font-size:13px; }}
      .decision-bottom {{ padding:18px 22px 22px; border-top:1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.02); }}
      .pill-stack {{ display:flex; flex-wrap:wrap; gap:8px; }}
      .pill {{
        display:inline-flex; padding:7px 10px; border-radius:999px; background: rgba(124,207,255,0.08); color:var(--blue);
        font-size:10px; font-weight:800; letter-spacing:.12em; text-transform:uppercase;
      }}
      .badge {{
        display:inline-flex; padding:8px 12px; border-radius:999px; font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.16em;
      }}
      .ready {{ color:var(--green); background: rgba(99,217,166,0.12); border:1px solid rgba(99,217,166,0.14); }}
      .watch {{ color:var(--amber); background: rgba(243,195,110,0.12); border:1px solid rgba(243,195,110,0.14); }}
      .recover {{ color:var(--red); background: rgba(255,135,150,0.12); border:1px solid rgba(255,135,150,0.14); }}
      .code {{
        border-radius:22px; border:1px solid rgba(255,255,255,0.08); background: rgba(2,6,12,0.9); overflow:hidden;
      }}
      .code-head {{
        padding:16px 18px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03);
      }}
      .lights {{ display:flex; gap:8px; }}
      .lights i {{ width:11px; height:11px; display:block; border-radius:999px; }}
      .lights i:nth-child(1) {{ background: rgba(255,135,150,0.7); }}
      .lights i:nth-child(2) {{ background: rgba(243,195,110,0.7); }}
      .lights i:nth-child(3) {{ background: rgba(99,217,166,0.7); }}
      pre {{ margin:0; padding:18px; white-space:pre-wrap; overflow:auto; color:#dce8fb; font-size:13px; line-height:1.58; font-family:"Cascadia Code", Consolas, monospace; }}
      table {{ width:100%; border-collapse:collapse; }}
      th, td {{ text-align:left; padding:14px 12px; border-bottom:1px solid rgba(255,255,255,0.06); vertical-align:top; }}
      th {{ color:#7f93ad; font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.14em; }}
      td {{ font-size:13px; color:var(--text); }}
      .timeline-item + .timeline-item {{ margin-top:16px; }}
      .timeline-item strong {{ display:block; font-size:15px; }}
      .timeline-item span {{ display:block; margin-top:6px; color:var(--muted); font-size:12px; line-height:1.5; }}
      .footer {{ display:flex; flex-wrap:wrap; gap:18px; margin:18px 0 8px; color:#7388a6; font-size:10px; text-transform:uppercase; letter-spacing:.16em; }}
      .footer strong {{ color:#c2d1e3; }}
      @media (max-width:1200px) {{
        .shell {{ grid-template-columns:1fr; }}
        .sidebar {{ display:none; }}
        .hero-grid, .hero-kpis, .grid-4, .grid-3, .grid-2 {{ grid-template-columns:1fr; }}
        .topbar {{ flex-direction:column; align-items:flex-start; position:static; }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <aside class="sidebar">
        <div>
          <div class="brand">
            <div class="mark">DM</div>
            <div>
              <strong>Decision Memory Engine</strong>
              <span>Context recovery // v1.0</span>
            </div>
          </div>
          <div class="nav">{nav_links}</div>
        </div>
        <div class="sidecard">
          <div class="k">Lead recommendation</div>
          <div class="v">{escape(summary["leadRecommendation"])}</div>
        </div>
      </aside>
      <main class="main">
        <div class="topbar">
          <div class="status"><span class="dot"></span>Decision recall registry live</div>
          <div class="meta-row">
            <div class="meta-box"><span>Watch decisions</span><strong>{summary["watchDecisions"]} active lanes</strong></div>
            <div class="meta-box"><span>Stale assumptions</span><strong>{summary["staleAssumptionLanes"]} decision chains</strong></div>
            <div class="meta-box"><span>Average confidence</span><strong>{summary["avgConfidence"]:.2f} baseline</strong></div>
          </div>
        </div>
        <section class="hero">
          <div class="hero-grid">
            <div class="hero-copy">
              <div class="eyebrow">Decision Memory Engine</div>
              <h1>{escape(title)}</h1>
              <p>{escape(subtitle)}</p>
              <div class="tabs">{top_tabs}</div>
            </div>
            <div class="hero-callout">
              <h3>Why this matters</h3>
              <p>Teams usually remember the headline decision, not the assumptions, evidence chain, or expiry conditions that made it safe in the first place.</p>
            </div>
          </div>
          <div class="hero-kpis">
            <div class="hero-kpi"><div class="label">Decisions</div><div class="value">{summary["decisionCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Watch lanes</div><div class="value">{summary["watchDecisions"]}</div></div>
            <div class="hero-kpi"><div class="label">Stale assumptions</div><div class="value">{summary["staleAssumptionLanes"]}</div></div>
            <div class="hero-kpi"><div class="label">Owners</div><div class="value">{summary["ownerCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Avg confidence</div><div class="value">{summary["avgConfidence"]:.2f}</div></div>
          </div>
        </section>
        {body}
        <div class="footer">
          <span><strong>Discipline:</strong> decision intelligence</span>
          <span><strong>Focus:</strong> rationale / stale assumptions / recall safety</span>
          <span><strong>Surface:</strong> operator-first / briefing-safe / replayable</span>
        </div>
      </main>
    </div>
  </body>
</html>"""


def render_overview() -> str:
    decisions = DecisionMemoryService.decisions()
    lanes = DecisionMemoryService.owner_lanes()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Control-plane summary</div>
          <h2>Decisions age faster than people think, especially when the assumptions move underneath them.</h2>
          <p>This engine tracks reusable decisions as memory artifacts so operators can recover the rationale, know what went stale, and decide whether a briefing should still inherit the old logic.</p>
        </div>
        <div class="section-body">
          <div class="grid-4">
            <div class="card"><div class="label">Ready decisions</div><div class="value">{len([d for d in decisions if d["status"] == "ready"])}</div><p>Decisions still safe to reuse with minimal context refresh.</p></div>
            <div class="card"><div class="label">Watch decisions</div><div class="value">{len([d for d in decisions if d["status"] == "watch"])}</div><p>Reusable, but carrying stale assumptions or new evidence pressure.</p></div>
            <div class="card"><div class="label">Recover lanes</div><div class="value">{len([d for d in decisions if d["status"] == "recover"])}</div><p>Decisions that should be reconstructed before they enter another briefing.</p></div>
            <div class="card"><div class="label">Owner lanes</div><div class="value">{len(lanes)}</div><p>Distinct stewardship lanes responsible for decision-memory upkeep.</p></div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div class="kicker">Recent decision memory</div>
          <h2>The highest-risk decision chains stay visible as an operator board.</h2>
          <p>The point is not just to remember what was decided. It is to remember why, under what assumptions, and whether those assumptions still deserve trust.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">
            {"".join(render_decision_card(decision) for decision in decisions[:2])}
          </div>
        </div>
      </section>
    """
    return shell(
        "Store rationale, not just outcomes.",
        "A Python and FastAPI decision engine for storing prior decisions, rationale, confidence, stale assumptions, and operator context recovery.",
        "overview",
        body,
    )


def render_memory_board() -> str:
    cards = "".join(render_decision_card(decision) for decision in DecisionMemoryService.decisions())
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Memory board</div>
          <h2>Decision records ordered by where semantic drift is most likely to hurt the next move.</h2>
          <p>Each card ties the original rationale to owner lane, expiry window, and stale-assumption pressure so teams can reuse judgment more safely.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">{cards}</div>
        </div>
      </section>
    """
    return shell(
        "Decision records with the assumptions that made them safe.",
        "A Python and FastAPI decision engine for storing prior decisions, rationale, confidence, stale assumptions, and operator context recovery.",
        "memory-board",
        body,
    )


def render_replay() -> str:
    timeline = DecisionMemoryService.timeline()
    sample = DecisionMemoryService.evaluate(
        {
            "prompt": "Need platform migration decision context for board review and release gate",
            "freshness_budget_days": 30,
        }
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Decision replay</div>
          <h2>Replay the reasoning path before a team blindly repeats the old move.</h2>
          <p>The replay surface makes it obvious which rationale chain will be recovered first, what stale assumptions it carries, and how much of the old context still survives.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">
            <div class="panel">
              <div class="label">Timeline</div>
              <div class="timeline">
                {"".join(
                    f'<div class="timeline-item"><strong>{escape(item["title"])}</strong><span>{escape(item["decidedAt"])} · next review {escape(item["nextReview"])} · {escape(item["status"])} · stale signals {item["staleSignalCount"]}</span></div>'
                    for item in timeline
                )}
              </div>
            </div>
            <div class="code">
              <div class="code-head"><span class="label" style="color:#92d9ff;">POST /api/analyze/recollection</span><div class="lights"><i></i><i></i><i></i></div></div>
              <pre>{escape(str(sample))}</pre>
            </div>
          </div>
        </div>
      </section>
    """
    return shell(
        "Replay the decision path before briefing distribution.",
        "A Python and FastAPI decision engine for storing prior decisions, rationale, confidence, stale assumptions, and operator context recovery.",
        "replay",
        body,
    )


def render_owners() -> str:
    lanes = DecisionMemoryService.owner_lanes()
    owner_cards = "".join(render_owner_card(lane) for lane in lanes)
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Owner lanes</div>
          <h2>Decision stewardship becomes visible when ownership pressure is explicit.</h2>
          <p>Owner lanes reveal which teams are carrying the most fragile memory artifacts and which decisions deserve a review before they are reused in operating or executive contexts.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">
            {owner_cards}
          </div>
        </div>
      </section>
    """
    return shell(
        "Owner lanes for decision stewardship and review pressure.",
        "A Python and FastAPI decision engine for storing prior decisions, rationale, confidence, stale assumptions, and operator context recovery.",
        "owners",
        body,
    )


def render_docs() -> str:
    sample = DecisionMemoryService.sample_decision()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">API summary</div>
          <h2>A small route surface for decision recall, replay, and operator-safe reuse.</h2>
          <p>The engine exposes the minimum useful surface for storing decisions, ranking reusable context, and showing where assumptions have started to drift.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">
            <div class="card"><div class="label">GET /api/decisions</div><div class="value" style="font-size:22px;">Decision board</div><p>Returns decisions ordered by recovery pressure and next review window.</p></div>
            <div class="card"><div class="label">GET /api/timeline</div><div class="value" style="font-size:22px;">Replay lane</div><p>Returns a chronological replay surface for decision-memory review.</p></div>
            <div class="card"><div class="label">POST /api/analyze/recollection</div><div class="value" style="font-size:22px;">Recall scoring</div><p>Ranks prior decisions against a new prompt and freshness budget.</p></div>
          </div>
          <div class="code" style="margin-top:18px;">
            <div class="code-head"><span class="label" style="color:#92d9ff;">Sample decision</span><div class="lights"><i></i><i></i><i></i></div></div>
            <pre>{escape(str(sample))}</pre>
          </div>
        </div>
      </section>
    """
    return shell(
        "API surface for decision memory and rationale recovery.",
        "A Python and FastAPI decision engine for storing prior decisions, rationale, confidence, stale assumptions, and operator context recovery.",
        "docs",
        body,
    )


def render_decision_card(decision: dict[str, object]) -> str:
    stale = decision["stale_signals"]
    return f"""
      <div class="decision-card">
        <div class="decision-top">
          <div>
            <h3>{escape(str(decision["title"]))}</h3>
            <div class="meta">{escape(str(decision["owner"]))} · {escape(str(decision["domain"]))} · {escape(str(decision["decision_type"]))}</div>
          </div>
          {badge(str(decision["status"]), str(decision["status"]))}
        </div>
        <div class="decision-bottom">
          <p>{escape(str(decision["rationale"]))}</p>
          <div class="pill-stack" style="margin-top:14px;">
            {"".join(f'<span class="pill">{escape(source)}</span>' for source in decision["sources"])}
          </div>
          <div class="pill-stack" style="margin-top:10px;">
            {"".join(f'<span class="pill">{escape(signal)}</span>' for signal in stale) or '<span class="pill">No stale assumptions flagged</span>'}
          </div>
        </div>
      </div>
    """


def render_owner_card(lane: dict[str, object]) -> str:
    domains = "".join(
        f"<span class='pill'>{escape(str(domain))}</span>" for domain in lane["domains"]
    )
    return f"""
      <div class="card">
        <div class="label">Owner lane</div>
        <div class="value" style="font-size:26px;">{escape(str(lane["owner"]))}</div>
        <p>{lane["decisionCount"]} decisions · {lane["watchCount"]} active watch lanes</p>
        <div class="pill-stack" style="margin-top:14px;">{domains}</div>
        <p style="margin-top:14px;"><strong>Focus decision:</strong> {escape(str(lane["focusDecision"]))}</p>
      </div>
    """


def write_static_proof_pages(screenshot_dir: Path) -> list[Path]:
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-memory-board.html": render_memory_board(),
        "03-replay.html": render_replay(),
        "04-api-summary.html": render_docs(),
    }
    written = []
    for name, content in pages.items():
        page = screenshot_dir / name
        page.write_text(content, encoding="utf-8")
        written.append(page)
    return written
