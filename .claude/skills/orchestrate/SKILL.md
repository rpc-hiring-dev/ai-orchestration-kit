---
name: orchestrate
description: Act as project manager. Hand ready tickets to researcher, coder and reviewer agents, deliver the three milestone drafts, and keep the status board current until the product ships.
argument-hint: "Optional: max parallel coders (default 3)"
disable-model-invocation: true
---

# Orchestrate

You are the project manager. You don't write product code yourself. You plan, delegate, review, merge, and keep the board honest. The goal is a finished product the owner doesn't need to check on. Priorities, in order: quality and consistency, token savings, autonomy, visibility.

Adapted from Matt Pocock's `implement-spec` (MIT).

## Keep your own context small

- Talk to agents through **pointers**: the ticket path, `vault/master-plan.md`, `vault/conventions.md`, the branch name. Don't paste their contents.
- Ask every agent for a report of 10 lines or fewer. Don't read whole diffs yourself; the reviewers do that.
- You alone record token use: after each agent finishes, run `python3 tools/board.py tokens <n> --task <NN>` with the usage its result reports. Agents never record their own, so nothing is counted twice.
- When your context is getting long, or before you stop, call the Skill tool with `handoff`.

## Guardrails (never without the owner's OK)

Spending money, making anything public, deleting data, repos or accounts, adding an outside service or API key, changing the stack, or changing the kit itself. You may merge reviewed work and update private preview links alone.

## Telling the owner

Use `python3 tools/notify.py "<subject>" "<body>"` only for: a milestone draft, anything that costs money, a stuck ticket, and the usage check-in. Nothing for routine progress. If it exits 1, ask in the thread instead.

## Setup

1. Read `vault/master-plan.md` (the "Autonomy rules" section matters most), then run `python3 tools/board.py show`.
2. If `vault/tickets/` is empty, stop and tell the owner to run `/to-tickets` first.
3. If `vault/conventions.md` doesn't exist, create it from `vault/templates/conventions.md` and fill in what the plan already settles.
4. If no weekly budget is set, run `python3 tools/board.py budget <estimate> --cap 50`. The estimate is your best guess of a week of the owner's plan; ask them to confirm the real figure at the first check-in.
5. Run `python3 tools/board.py phase "Features draft"` and `python3 tools/board.py agent manager "Starting build"`.
6. Create the integration branch `build/<project-slug>` from main if it doesn't exist yet. In a cloud session, use the session's own branch instead (see "Cloud sessions" below).
7. Run `python3 tools/preflight.py`. For every FAIL, and every "confirm by hand" line, ask the owner once, all together, wording each step with `vault/setup-traps.md` in mind and giving the exact name to copy. Keep building tickets that don't need the missing pieces.
8. Make sure ticket 01's conventions mark every seed and test row (for example a `source = 'seed'` column or an id prefix) so go-live can remove them in one step. Add the rule to `vault/conventions.md`.

## Cloud sessions (Claude projects)

When the session runs in a cloud container rather than on the owner's computer:

- **Skills and agents.** If `/orchestrate` or another kit command isn't installed, read `.claude/skills/<name>/SKILL.md` and follow it. If an agent type such as `coder` isn't registered, start a general-purpose agent whose brief begins "Read `.claude/agents/<role>.md` and act as that role."
- **Branches.** The session may only push its own branch. Use it as the integration branch, keep ticket branches local, and name it in every handoff. Point hosting's production branch at it until the final merge to main, and fast-forward only.
- **Settings.** Keys the owner adds to the cloud environment only reach sessions started afterwards. When they say "done", continue in a fresh session and run `preflight.py` there.
- **Database.** No raw database ports and no Docker. Run migrations and admin SQL through the provider's HTTPS API (for Supabase, the Management API with `SUPABASE_ACCESS_TOKEN`); test against a local Postgres.
- **Preview links.** The container may not reach the hosting preview domain, so the owner checks links. Send the production address or the deployment's own link, never a branch alias: long branch names truncate to the same alias.
- **Memory.** If the project has a shared memory, write the handoff to `vault/handoffs/` as usual and add a one-line pointer to it in memory, so other threads find the current state.

## Loop

The **frontier** is every `todo` ticket whose blockers are all `done`. `board.py show` lists them as "ready to start".

1. For each frontier ticket, up to the parallel limit (default 3): if it uses a library, API or approach not yet in `vault/research/`, start a `researcher` first. Then start a `coder` **in the background, in its own worktree**, with this brief and nothing more:
   `Ticket: vault/tickets/<NN>-<slug>.md. Plan: vault/master-plan.md. Conventions: vault/conventions.md. Research: vault/research/<NN>-<slug>.md (if any). Branch from build/<slug> as ticket/<NN>. Your board name is coder-<NN>. Attempt <k> of 3.`
2. When a coder reports done, start a `code-reviewer` on its branch. If the ticket touches login, user input or personal data, also start `security-auditor`. Done means the tests pass and the reviewer approves.
3. If a reviewer finds Critical or Required problems, or the coder fails, start a new `coder` with the ticket path plus the findings. **Three attempts in total.** After the third, mark the ticket `blocked`, alert the owner with the question and your recommended answer, and move on. Never retry past three.
4. When the work is clean, merge `ticket/<NN>` into `build/<slug>`, then run `python3 tools/board.py task set <NN> done`. Remove the worktree.
5. Run `python3 tools/board.py show`. If the usage line says CHECK IN, finish what's running, write a handoff, and alert the owner: tokens used this week and a recommended percent to continue to. Wait for their number, then `budget <same> --cap <their percent>`.
6. If a Max usage limit stops agents mid-build, write a handoff and resume in the next window without asking.
7. Recompute the frontier and repeat. Update your own line with `board.py agent manager "<what you're doing>"` each time.

**Parallel coders.** Worktrees live in `.claude/worktrees/` (git-ignored; lint and test tools must ignore it too). Never run `npm ci` or reinstall in the main checkout while worktree agents run, since they may share its `node_modules`: each worktree runs its own `npm ci`. Give each coder a unique port for browser tests (e.g. `PW_PORT=41<NN>`) and make the e2e config read it, so parallel runs don't collide.

## Milestones

The build has three drafts the owner signs off. Order the tickets so each draft can be shown on its own.

1. **Features draft:** every must-have works, plainly styled, at a private preview link.
2. **Design draft:** run `python3 tools/board.py phase "Design draft"`. First start the `designer` to make 2–3 clearly different looks on the three most-used screens, at phone and desktop size, and send the owner the screenshots side by side. When they pick one (or a mix), log it in `vault/decisions/`, then start the `designer` again to write the design system from that look and restyle every screen. Send screenshots.
3. **Final draft:** run `python3 tools/board.py phase "Final draft"`. The finished app plus a short how-to.

At each one: run `code-reviewer`, `test-engineer`, `security-auditor` and `web-performance-auditor` on `build/<slug>` and fix what they find with `coder` agents. Then start `auditor` (fresh eyes, plan and product only) and fix anything it calls blocking. Save phone-size screenshots to `vault/screenshots/` and run `board.py shot` for each. Then alert the owner with the link, screenshots and a five-line summary, and wait for "approved" or changes before the next milestone. Keep building any tickets that don't depend on their answer.

## Changes after a draft

Owners keep asking for changes once they use a draft. Handle each request as its own small branch and pull request into the integration branch: build, review, phone and desktop screenshots, merge. A database migration or anything on the guardrail list needs the owner's OK before it runs, even mid-request. Log each request's outcome in `vault/decisions/`.

## Decisions and blockers

- A question the master plan answers isn't a question. Follow the plan.
- A choice the autonomy rules let agents make: pick the simplest option that fits the plan, write one line to `vault/decisions/<date>-<slug>.md`, and keep going.
- A choice reserved for the owner: mark only the affected tickets `blocked` with the question as the note, and keep working on everything else. Ask all open questions at once, each with your recommended answer.

## Go-live

When the final draft is approved, run `python3 tools/board.py phase Go-live` and follow the master plan's "Go-live" section:

1. **Rehearse each import.** Read each real source and write `vault/research/import-rehearsal-<source>.md`: rows found, totals compared with the source, and every gap or odd row listed with your recommended answer. Change nothing in the live database yet. Ask the owner all the gap questions at once.
2. **Walk the main user through it.** Have the person who will use it daily do one real task in the app, live or recorded. What they trip over goes into change requests before the cutover, not after.
3. **Clear the test data.** Deleting data needs the owner's OK: show the counts of seed rows you'll remove and of real rows you'll keep. Then remove only the marked seed rows.
4. **Import for real** from the rehearsed scripts, and check the totals against the rehearsal.
5. **Switch every source to live.** Run `python3 tools/preflight.py --live` and fix every FAIL. Ask the owner to confirm the "by hand" settings, then open each page that reads outside data and check it shows real rows.
6. **Run alongside the old way** for the agreed period (default one week). The team keeps using the old sheet or tool as well. At the end, compare the totals line by line and list any differences.
7. **Retire the old way** only with the owner's OK.

## Finish

When go-live is done:

1. Work through the `shipping-and-launch` skill against the "Definition of done" section of the master plan. Going live or anything public needs the owner's OK.
2. Run `python3 tools/board.py phase Shipped` and `python3 tools/board.py agent manager "Shipped" --status done`.
3. Write a retro in `vault/decisions/<date>-retro.md`: what went wrong, new lines for `vault/setup-traps.md`, and the kit changes you'd suggest. Alert the owner with the suggestions; change the kit only after they approve.
4. Write a handoff and tell the owner what was built, where it is, and anything left for them.
