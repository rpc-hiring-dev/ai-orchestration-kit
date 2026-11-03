# Working in this repo

This repo is an agent team. The owner describes a product once, and agents plan it, build it and report progress without being checked on.

## The workflow
1. `/kickoff`: interview the owner and write `vault/master-plan.md`.
2. `/to-tickets`: split the approved plan into tickets in `vault/tickets/`.
3. `/orchestrate`: the main session becomes the project manager and runs researcher, coder, designer, reviewer and auditor agents through three milestone drafts (features, design, final) the owner signs off, then go-live (import rehearsal, real data, a parallel run with the old way).
   In a cloud session where these commands aren't installed, read `.claude/skills/<name>/SKILL.md` and follow it.
4. `/feature`: after a draft or after launch, each change the owner asks for runs in its own thread: branch, pull request with before-and-after screenshots, the owner's OK to merge, then each live step with its own OK.
5. `/handoff`: write a handoff note before any session ends.

## Where things live
- `vault/` is the Obsidian vault and the single source of truth: master plan, conventions, specs, tickets, research notes, decisions, handoffs and screenshots.
- `vault/system-plan.md` holds the owner's standing answers for every product (stack, guardrails, milestones, alerts). The owner's name is at its top; skills say "the owner".
- `env.manifest` lists every key and setting the product needs (names only). `tools/preflight.py` checks them; `vault/setup-traps.md` lists setup mistakes to avoid.
- `tools/board.py` is the status board, including token use and the screenshot timeline. Every agent reports through it, and nobody edits `status/board.json` by hand.
- `tools/notify.py` alerts the owner (Telegram push, email, or both), only for milestone drafts, money, stuck tickets and the usage check-in.
- `vault/Dashboard.md` and `dashboard/index.html` are generated views of the board.
- `vault/project-memory.md` says how to keep the shared project memory (Claude projects) as the running state once threads stop writing handoffs.

## Tracker
The issue tracker is local files. Specs go in `vault/specs/<slug>.md`, tickets in `vault/tickets/<NN>-<slug>.md`, and the triage label is `ready-for-agent`. Ignore any mention of `/setup-matt-pocock-skills`.

## Rules for every session
- The newest file in `vault/handoffs/` is loaded at session start. Trust it, and only read what it points to when the work needs it.
- Find facts yourself. Ask the owner only for decisions, and always offer a recommended answer.
- Follow the master plan. If it doesn't cover something, use its "Autonomy rules" to decide whether to choose or ask.
- Record decisions as one line each in `vault/decisions/`.
- Keep reports short. Point to files instead of pasting them.
- Never commit secrets or contact details. They go in `.env`, which is git-ignored.
- Never without the owner's OK: spend money, make anything public, delete data, repos or accounts, add an outside service or key, change the stack, or change the kit.
- **Live changes:** once real people use the product, nothing is merged to the branch that deploys it, no migration runs on its database, no function is deployed, no secret is set and no email, scheduled job or webhook is switched on without the owner's OK for that change. Test migrations on a local copy first. Afterwards, reply with a short "What went live" list.
- Before stopping, or when context is getting long, run `/handoff`.
