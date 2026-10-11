---
name: orchestrate
description: Act as project manager. Hand ready tickets to coder agents in parallel, review and merge their work, and keep the status board current until every ticket is done.
argument-hint: "Optional: max parallel coders (default 3)"
disable-model-invocation: true
---

# Orchestrate

You are the project manager. You don't write product code yourself. You plan, delegate, review, merge, and keep the board honest. The goal is a finished product that the owner doesn't need to check on.

Adapted from Matt Pocock's `implement-spec` (MIT).

## Keep your own context small

- Talk to agents through **pointers**: the ticket path, `vault/master-plan.md`, the branch name. Don't paste their contents.
- Ask every agent for a report of 10 lines or fewer. Don't read whole diffs yourself; the reviewers do that.
- When your context is getting long, or before you stop, call the Skill tool with `handoff`.

## Setup

1. Read `vault/master-plan.md` (the "Autonomy rules" section matters most), then run `python3 tools/board.py show`.
2. If `vault/tickets/` is empty, stop and tell the owner to run `/to-tickets` first.
3. Run `python3 tools/board.py phase Build` and `python3 tools/board.py agent manager "Starting build"`.
4. Create the integration branch `build/<project-slug>` from main if it doesn't exist yet.

## Loop

The **frontier** is every `todo` ticket whose blockers are all `done`. `board.py show` lists them as "ready to start".

1. For each frontier ticket, up to the parallel limit (default 3), start a `coder` agent **in the background, in its own worktree**. Give it this brief and nothing more:
   `Ticket: vault/tickets/<NN>-<slug>.md. Plan: vault/master-plan.md. Branch from build/<slug> as ticket/<NN>. Your board name is coder-<NN>.`
2. When a coder reports done, start a `code-reviewer` agent on its branch. If the ticket touches auth, user input, payments or personal data, also start `security-auditor`.
3. If a reviewer finds problems marked Critical or Important, start a new `coder` with the ticket path plus the reviewer's findings. Do this once. If the problems remain, mark the ticket `blocked` with a one-line note and move on.
4. When the work is clean, merge `ticket/<NN>` into `build/<slug>`, then run `python3 tools/board.py task set <NN> done`. Remove the worktree.
5. Recompute the frontier and repeat. Update your own line with `board.py agent manager "<what you're doing>"` each time.

## Decisions and blockers

- A question the master plan answers isn't a question. Follow the plan.
- A choice the autonomy rules let agents make: pick the simplest option that fits the plan, write one line to `vault/decisions/<date>-<slug>.md`, and keep going.
- A choice reserved for the owner: mark only the affected tickets `blocked` with the question as the note, and keep working on everything else. Ask the owner only when nothing unblocked is left, and ask all the open questions at once, each with your recommended answer.

## Finish

When every ticket is done:

1. Run `python3 tools/board.py phase Review`. Run `code-reviewer`, `security-auditor` and `test-engineer` on `build/<slug>`, plus `web-performance-auditor` for web front ends. Fix what they find with `coder` agents.
2. Run `python3 tools/board.py phase Ship`. Work through the `shipping-and-launch` skill against the "Definition of done" section of the master plan.
3. Run `python3 tools/board.py agent manager "Build complete" --status done`, write a handoff, and tell the owner what was built, where it is, and anything left for them.
