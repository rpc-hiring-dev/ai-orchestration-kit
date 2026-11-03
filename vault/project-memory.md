# Project memory

In Claude projects every thread shares one project memory. Once a build moves to one thread per change (`/feature`), threads stop writing handoffs, and this memory becomes the running state of the product. These rules keep it useful. On a laptop with no shared memory, the newest file in `vault/handoffs/` plays the same role.

## Shape
- **One summary file** (the memory index) that a new thread can read in a minute: setup and accounts, how the app works, open asks for the owner, and one line per feature.
- **One file per subject** for anything longer (a feature with many moving parts, the build state, the owner's working preferences). Link it from its summary line.
- Keep each file under about 4 KB. When one grows past that, summarise it; don't start a second file on the same subject.

## A feature line
`<Feature> (PR #<n>, <state> <date>, <who OK'd>): <one line on what it does>. <Migration name, function or schedule if any>.`

States, in order: **PR open**, **merged**, **LIVE**. Write LIVE only after the live steps ran and were checked. Update the same line as the state changes. Example:
`Task history (PR #48 merged + LIVE 2026-11-02, migration 20261102120000 applied with Liam's OK): records who entered, edited and completed each task.`

## What goes in
- Decisions the owner made that a new thread would otherwise ask again, with the date.
- Where things are: accounts, project folder files, runbooks, which branch builds production.
- Gotchas that cost time. Also add them to `vault/setup-traps.md` so the next product gets them.
- Open asks for the owner, removed once answered.

## What stays out
- Keys, passwords, phone numbers and email addresses. Point to where they live ("in Settings", "in the owner's password manager").
- What the repo already records: code structure, commit history, the master plan.
- Relative dates. Write "2026-11-02", never "yesterday".
