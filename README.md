# AI orchestration kit

A starter repo for building software with a team of Claude agents. You describe what you want once, and the agents interview you, write a master plan, split it into tickets, build them in parallel, review the work, and show their progress on a live board.

## How a project runs

| Step | You run | What happens |
|---|---|---|
| 1 | `/kickoff <one line idea>` | Claude interviews you in rounds of numbered questions, each with a recommended answer, until nothing is left assumed. Then it writes `vault/master-plan.md` for you to approve. |
| 2 | `/to-tickets` | The plan becomes small tickets in `vault/tickets/`, each listing what blocks it. You approve the breakdown. |
| 3 | `/orchestrate` | The session becomes the project manager. A researcher prepares each ticket, up to 3 coders build in parallel, reviewers check each branch, and an auditor with fresh eyes checks each milestone. |
| 4 | Approve 3 drafts | You get an email at the features, design and final drafts, and whenever something costs money or a ticket is stuck after 3 attempts. Otherwise watch `dashboard/index.html` or the Dashboard note in Obsidian: tasks, agents, token use and a screenshot timeline. |
| 5 | `/handoff` | Writes a short note. The next session starts by reading it, so it doesn't need old chat history. |

## What's inside

```
CLAUDE.md                  short rules loaded into every session
.claude/
  settings.json            session-start hook (loads the latest handoff and the board)
  skills/                  kickoff, orchestrate, handoff + vendored skills (see THIRD_PARTY.md)
  agents/                  researcher, coder, designer, auditor, code-reviewer, security-auditor, test-engineer, web-performance-auditor
tools/board.py             the status board every agent reports to (tasks, tokens, screenshots)
tools/notify.py            emails the owner through Resend's free tier
.env.example               copy to .env for the email key and address
vault/                     open this folder in Obsidian
  Home.md, Dashboard.md, system-plan.md, master-plan.md, conventions.md, specs/, tickets/,
  research/, decisions/, handoffs/, screenshots/, Parked tools.md
dashboard/index.html       browser dashboard, refreshes every 15s
status/board.json          board data, written only by board.py
```

## Why it's cheap on tokens

- **Skills load on demand.** Most skills here are user-invoked only (`/kickoff`, `/to-tickets`, and so on), so they cost nothing until you run them. The others add only a one-line description until they're used.
- **CLAUDE.md is short.** It loads every session, so it holds rules and pointers, not content.
- **Coders get fresh contexts.** Each ticket runs in its own agent with only the ticket and the relevant part of the plan. The manager sees 10-line reports, not diffs.
- **Handoffs replace history.** Every session starts clean, with one short note instead of a long transcript.
- **No always-on connectors.** Design tools and other connectors are parked in `vault/Parked tools.md` and added per project.

## Using it

- **Claude Code on your computer:** clone the repo, run `claude` in it, then `/kickoff`. Open `vault/` in Obsidian to read and edit the plan, tickets and dashboard.
- **Claude projects (claude.ai):** attach this repo to the project. Every thread is a Claude Code session that loads these skills, agents and hooks.
- **A new product:** on GitHub, mark this repo as a template, then click "Use this template" for each new product. Every product gets its own copy of the kit and its own vault.

Needs Python 3 for `tools/board.py` and `tools/notify.py`. They use only the standard library. For email alerts, make a free account at resend.com with the address you want alerts sent to, then put the key and address in `.env`.
