#!/usr/bin/env python3
"""Status board for the agent team.

Every agent reports through this script. Each change rewrites:
  status/board.json      source of truth
  vault/Dashboard.md     the board inside Obsidian
  dashboard/index.html   a self-refreshing page you can open in any browser

Usage:
  board.py init "<project name>"
  board.py phase <name|number>                    set the current phase
  board.py task add <id> "<title>" [--blocked-by 01,02] [--est TOKENS]
  board.py task set <id> <todo|doing|review|done|blocked> [--agent NAME] [--note TEXT] [--tokens N]
  board.py agent <name> "<what it is doing>" [--status working|idle|blocked|done] [--tokens N]
  board.py tokens <n> [--task ID]                 record tokens used (adds to the totals)
  board.py budget <weekly tokens> [--cap 50]      weekly token budget and check-in point in percent
  board.py shot <image path> "<caption>"          add a build screenshot to the timeline
  board.py show [--brief]
  board.py render
"""
import argparse
import datetime as dt
import html
import json
import os
import sys
from contextlib import contextmanager

try:
    import fcntl  # not available on Windows; locking is skipped there
except ImportError:
    fcntl = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "status", "board.json")
LOCK = os.path.join(ROOT, "status", ".board.lock")
MD = os.path.join(ROOT, "vault", "Dashboard.md")
HTML = os.path.join(ROOT, "dashboard", "index.html")

PHASES = ["Discovery", "Master plan", "Tickets", "Features draft", "Design draft", "Final draft", "Shipped"]
TASK_STATES = ["todo", "doing", "review", "done", "blocked"]
AGENT_STATES = ["working", "idle", "blocked", "done"]


def now():
    return dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")


def empty(project="Untitled project"):
    return {"project": project, "phase": PHASES[0], "phases": PHASES,
            "tasks": {}, "agents": {}, "log": [], "updated": now(),
            "tokens": [], "budget": None, "cap": 50, "shots": []}


def tokens_used(board, days=None):
    """Actual tokens recorded, optionally only in the last `days` days."""
    since = (dt.datetime.now() - dt.timedelta(days=days)).strftime("%Y-%m-%d") if days else ""
    return sum(t["n"] for t in board.get("tokens", []) if t["date"] >= since)


def usage_line(board):
    used, budget = tokens_used(board, 7), board.get("budget")
    if not budget:
        return f"{used:,} tokens in the last 7 days (no weekly budget set)"
    pct = round(100 * used / budget)
    flag = " - CHECK IN WITH THE OWNER" if pct >= board.get("cap", 50) else ""
    return f"{used:,} of {budget:,} weekly tokens ({pct}%, check-in at {board.get('cap', 50)}%){flag}"


def add_tokens(board, n, task=None):
    board.setdefault("tokens", []).append({"date": now(), "n": n, "task": task})
    if task in board["tasks"]:
        board["tasks"][task]["actual"] = board["tasks"][task].get("actual", 0) + n


@contextmanager
def locked_board():
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(LOCK, "w") as lock:
        if fcntl:
            fcntl.flock(lock, fcntl.LOCK_EX)
        board = {**empty(), **json.load(open(DATA))} if os.path.exists(DATA) else empty()
        board["phases"] = PHASES  # boards from older kits keep working with the current phases
        yield board
        board["updated"] = now()
        board["log"] = board["log"][-50:]
        tmp = DATA + ".tmp"
        with open(tmp, "w") as f:
            json.dump(board, f, indent=2)
        os.replace(tmp, DATA)
        render(board)


def progress(board):
    tasks = board["tasks"].values()
    done = sum(t["status"] == "done" for t in tasks)
    return done, len(board["tasks"])


def ready(board, task):
    return all(board["tasks"].get(b, {}).get("status") == "done" for b in task["blocked_by"])


def render(board):
    done, total = progress(board)
    pct = round(100 * done / total) if total else 0
    phase_i = board["phases"].index(board["phase"]) if board["phase"] in board["phases"] else 0
    est = sum(t.get("est") or 0 for t in board["tasks"].values())
    shots = board.get("shots", [])

    def cell(x):  # keep Obsidian tables intact
        return str(x or "").replace("|", "\\|").replace("\n", " ")

    # Obsidian dashboard
    lines = [f"# {board['project']}", "",
             f"**Phase:** {board['phase']} ({phase_i + 1} of {len(board['phases'])})  ",
             f"**Tasks done:** {done} of {total} ({pct}%)  ",
             f"**Tokens:** {tokens_used(board):,} used in total, estimate {est:,}  ",
             f"**This week:** {usage_line(board)}  ",
             f"**Updated:** {board['updated']}", "", "## Agents", ""]
    if board["agents"]:
        lines += ["| Agent | Status | Doing | Since |", "|---|---|---|---|"]
        lines += [f"| {cell(n)} | {a['status']} | {cell(a['doing'])} | {a['updated']} |" for n, a in sorted(board["agents"].items())]
    else:
        lines.append("_No agents have reported yet._")
    lines += ["", "## Tasks", ""]
    if board["tasks"]:
        lines += ["| # | Task | Status | Agent | Blocked by | Tokens est / actual | Note |", "|---|---|---|---|---|---|---|"]
        for tid, t in sorted(board["tasks"].items()):
            lines.append(f"| {cell(tid)} | {cell(t['title'])} | {t['status']} | {cell(t.get('agent'))} | "
                         f"{', '.join(t['blocked_by'])} | {t.get('est') or '-'} / {t.get('actual', 0)} | {cell(t.get('note'))} |")
    else:
        lines.append("_No tasks yet._")
    lines += ["", "## Build timeline", ""]
    lines += [f"**{s['date']}** {s['caption']}\n\n![[{s['path']}|360]]\n" for s in shots] or ["_No screenshots yet._"]
    lines += ["", "## Recent activity", ""] + [f"- {e}" for e in reversed(board["log"][-15:])]
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, "w").write("\n".join(lines) + "\n")

    # Browser dashboard
    e = html.escape
    steps = "".join(
        f'<li class="{"done" if i < phase_i else "now" if i == phase_i else ""}">{e(p)}</li>'
        for i, p in enumerate(board["phases"]))
    agents = "".join(
        f'<tr><td>{e(n)}</td><td><span class="pill {e(a["status"])}">{e(a["status"])}</span></td>'
        f'<td>{e(a["doing"])}</td><td class="muted">{e(a["updated"])}</td><td class="muted">{a.get("tokens", 0):,}</td></tr>'
        for n, a in sorted(board["agents"].items())) or '<tr><td colspan="5" class="muted">No agents have reported yet.</td></tr>'
    cols = ""
    for state in TASK_STATES:
        cards = "".join(
            f'<div class="card"><b>{e(tid)}</b> {e(t["title"])}'
            f'{"<div class=muted>" + e(t["agent"]) + "</div>" if t.get("agent") else ""}'
            f'{"<div class=muted>" + e(t["note"]) + "</div>" if t.get("note") else ""}'
            f'<div class=muted>tokens {format(t["est"], ",") if t.get("est") else "-"} est / {t.get("actual", 0):,} actual</div>'
            f'{"<div class=muted>waits on " + e(", ".join(t["blocked_by"])) + "</div>" if state == "todo" and not ready(board, t) else ""}</div>'
            for tid, t in sorted(board["tasks"].items()) if t["status"] == state)
        n = sum(t["status"] == state for t in board["tasks"].values())
        cols += f'<section class="col"><h3>{state} <span class="muted">{n}</span></h3>{cards}</section>'
    log = "".join(f"<li>{e(x)}</li>" for x in reversed(board["log"][-15:]))
    timeline = "".join(
        f'<figure><img src="../vault/{e(s["path"])}" alt="{e(s["caption"])}" loading="lazy">'
        f'<figcaption><b>{e(s["date"])}</b> {e(s["caption"])}</figcaption></figure>'
        for s in shots) or '<p class="muted">No screenshots yet. Agents add one at each milestone.</p>'
    total_tokens = tokens_used(board)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="15"><title>{e(board['project'])} board</title>
<style>
:root{{--bg:#fafaf9;--fg:#1c1917;--muted:#78716c;--card:#fff;--line:#e7e5e4;--accent:#2563eb;--ok:#16a34a;--warn:#d97706;--bad:#dc2626}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1c1917;--fg:#f5f5f4;--muted:#a8a29e;--card:#292524;--line:#44403c;--accent:#60a5fa;--ok:#4ade80;--warn:#fbbf24;--bad:#f87171}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}}
main{{max-width:1100px;margin:auto}} h1{{margin:0 0 4px}} .muted{{color:var(--muted);font-size:13px}}
.bar{{height:10px;background:var(--line);border-radius:5px;overflow:hidden;margin:12px 0}} .bar i{{display:block;height:100%;width:{pct}%;background:var(--ok)}}
ol.steps{{display:flex;flex-wrap:wrap;gap:6px;padding:0;list-style:none;margin:12px 0}}
ol.steps li{{padding:4px 10px;border:1px solid var(--line);border-radius:14px;font-size:13px;color:var(--muted)}}
ol.steps li.done{{color:var(--ok);border-color:var(--ok)}} ol.steps li.now{{color:#fff;background:var(--accent);border-color:var(--accent)}}
table{{width:100%;border-collapse:collapse;background:var(--card)}} td,th{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}}
.pill{{font-size:12px;padding:1px 8px;border-radius:10px;border:1px solid currentColor}}
.working{{color:var(--accent)}} .blocked{{color:var(--bad)}} .done{{color:var(--ok)}} .idle{{color:var(--muted)}}
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}}
.col{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}} .col h3{{margin:0 0 8px;font-size:14px;text-transform:capitalize}}
.card{{border:1px solid var(--line);border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:14px}}
.wrap{{overflow-x:auto}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin:12px 0}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 10px}} .stat b{{display:block;font-size:20px}}
.timeline{{display:flex;gap:12px;overflow-x:auto;padding-bottom:8px;scroll-snap-type:x mandatory}}
.timeline figure{{margin:0;flex:0 0 220px;scroll-snap-align:start;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px}}
.timeline img{{width:100%;border-radius:6px;display:block}} figcaption{{font-size:13px;margin-top:4px}}
</style></head><body><main>
<h1>{e(board['project'])}</h1>
<div class="muted">Phase {phase_i + 1} of {len(board['phases'])}: <b>{e(board['phase'])}</b> · {done} of {total} tasks done ({pct}%) · updated {e(board['updated'])} · refreshes every 15s</div>
<div class="bar"><i></i></div><ol class="steps">{steps}</ol>
<div class="stats"><div class="stat"><span class="muted">Tokens used</span><b>{total_tokens:,}</b></div>
<div class="stat"><span class="muted">Estimated</span><b>{est:,}</b></div>
<div class="stat"><span class="muted">This week</span><div>{e(usage_line(board))}</div></div></div>
<h2>Agents</h2><div class="wrap"><table><tr><th>Agent</th><th>Status</th><th>Doing</th><th>Since</th><th>Tokens</th></tr>{agents}</table></div>
<h2>Build timeline</h2><div class="timeline">{timeline}</div>
<h2>Tasks</h2><div class="cols">{cols}</div>
<h2>Recent activity</h2><ul class="muted">{log}</ul>
</main></body></html>
"""
    os.makedirs(os.path.dirname(HTML), exist_ok=True)
    open(HTML, "w").write(page)


def main(argv):
    p = argparse.ArgumentParser(description="Agent status board")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").add_argument("project")
    sub.add_parser("phase").add_argument("phase")
    task = sub.add_parser("task").add_subparsers(dest="action", required=True)
    add = task.add_parser("add")
    add.add_argument("id"); add.add_argument("title"); add.add_argument("--blocked-by", default="")
    add.add_argument("--est", type=int, help="estimated tokens")
    st = task.add_parser("set")
    st.add_argument("id"); st.add_argument("status", choices=TASK_STATES)
    st.add_argument("--agent"); st.add_argument("--note"); st.add_argument("--tokens", type=int, default=0)
    ag = sub.add_parser("agent")
    ag.add_argument("name"); ag.add_argument("doing")
    ag.add_argument("--status", choices=AGENT_STATES, default="working")
    ag.add_argument("--tokens", type=int, default=0)
    tk = sub.add_parser("tokens"); tk.add_argument("n", type=int); tk.add_argument("--task")
    bu = sub.add_parser("budget"); bu.add_argument("weekly", type=int); bu.add_argument("--cap", type=int, default=50)
    sh = sub.add_parser("shot"); sh.add_argument("path"); sh.add_argument("caption")
    sub.add_parser("show").add_argument("--brief", action="store_true")
    sub.add_parser("render")
    a = p.parse_args(argv)

    if a.cmd == "init":
        with locked_board() as b:
            b.clear(); b.update(empty(a.project)); b["log"].append(f"{now()} board started for {a.project}")
    elif a.cmd == "phase":
        with locked_board() as b:
            name = b["phases"][int(a.phase) - 1] if a.phase.isdigit() else a.phase
            if name not in b["phases"]:
                sys.exit(f"Unknown phase {name!r}. Phases: {', '.join(b['phases'])}")
            b["phase"] = name; b["log"].append(f"{now()} phase is now {name}")
    elif a.cmd == "task" and a.action == "add":
        with locked_board() as b:
            blockers = [x.strip() for x in a.blocked_by.split(",") if x.strip()]
            b["tasks"][a.id] = {"title": a.title, "status": "todo", "blocked_by": blockers,
                                "agent": None, "note": None, "updated": now(), "est": a.est, "actual": 0}
            b["log"].append(f"{now()} task {a.id} added: {a.title}")
    elif a.cmd == "task" and a.action == "set":
        with locked_board() as b:
            if a.id not in b["tasks"]:
                sys.exit(f"No task {a.id!r}. Add it first.")
            t = b["tasks"][a.id]
            t["status"] = a.status; t["updated"] = now()
            if a.agent: t["agent"] = a.agent
            if a.note is not None: t["note"] = a.note
            if a.tokens: add_tokens(b, a.tokens, a.id)
            b["log"].append(f"{now()} task {a.id} -> {a.status}" + (f" ({a.agent})" if a.agent else "")
                            + (f": {a.note}" if a.note else ""))
    elif a.cmd == "agent":
        with locked_board() as b:
            prev = b["agents"].get(a.name, {}).get("tokens", 0)
            b["agents"][a.name] = {"doing": a.doing, "status": a.status, "updated": now(), "tokens": prev + a.tokens}
            if a.tokens: add_tokens(b, a.tokens)
            b["log"].append(f"{now()} {a.name} [{a.status}] {a.doing}")
    elif a.cmd == "tokens":
        with locked_board() as b:
            add_tokens(b, a.n, a.task); b["log"].append(f"{now()} {a.n:,} tokens" + (f" on task {a.task}" if a.task else ""))
    elif a.cmd == "budget":
        if a.weekly <= 0 or not 0 < a.cap <= 100:
            sys.exit("Budget must be above 0 and --cap between 1 and 100.")
        with locked_board() as b:
            b["budget"], b["cap"] = a.weekly, a.cap; b["log"].append(f"{now()} weekly budget {a.weekly:,} tokens, check-in at {a.cap}%")
    elif a.cmd == "shot":
        if not os.path.isfile(a.path):
            sys.exit(f"No image at {a.path}.")
        shots_dir = os.path.join(ROOT, "vault", "screenshots")
        if os.path.commonpath([os.path.abspath(a.path), shots_dir]) != shots_dir:
            sys.exit("Screenshots must be saved in vault/screenshots/.")
        rel = os.path.relpath(os.path.abspath(a.path), os.path.join(ROOT, "vault"))
        with locked_board() as b:
            b["shots"].append({"date": now(), "path": rel.replace(os.sep, "/"), "caption": a.caption})
            b["log"].append(f"{now()} screenshot: {a.caption}")
    elif a.cmd == "render":
        with locked_board():
            pass
    elif a.cmd == "show":
        if not os.path.exists(DATA):
            print("No board yet. Start one with: python3 tools/board.py init \"<project>\"")
            return
        b = {**empty(), **json.load(open(DATA))}
        b["phases"] = PHASES
        done, total = progress(b)
        print(f"Board: {b['project']} | phase {b['phase']} | {done}/{total} tasks done | updated {b['updated']}")
        print(f"  usage: {usage_line(b)}")
        active = {k: t for k, t in b["tasks"].items() if t["status"] in ("doing", "review", "blocked")}
        nxt = [k for k, t in sorted(b["tasks"].items()) if t["status"] == "todo" and ready(b, t)]
        for k, t in sorted(active.items()):
            print(f"  {k} {t['status']}: {t['title']}" + (f" ({t['agent']})" if t.get("agent") else ""))
        if nxt:
            print(f"  ready to start: {', '.join(nxt)}")
        if not a.brief:
            for n, ag in sorted(b["agents"].items()):
                print(f"  agent {n} [{ag['status']}] {ag['doing']}")


if __name__ == "__main__":
    main(sys.argv[1:])
