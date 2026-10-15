# Conventions: <project name>

Every agent reads this first. The reviewer rejects work that breaks it. Keep it under 60 lines; change it only through the PM, and log each change in `vault/decisions/`.

## Stack
TypeScript and React. Installable web app (PWA), phone first. Changing the stack needs the owner.

## Naming
- Files and folders:
- Components:
- Database tables and columns:
- Tests:

## Structure
Where pages, components, data access and tests live.

## Design
Points to `vault/design-system.md` once the designer writes it. Icons: Tabler. Animation: GSAP only.

## Testing
Automated tests for logic, a click-through test of each main flow, and a screenshot check at phone size before a ticket is done.
Run e2e with a unique `PW_PORT` (e.g. 4100 + ticket number) when other agents may be running tests; the e2e config reads it.
Lint and test configs ignore `.claude/worktrees/`.

## Secrets
Keys and contact details go in `.env`, never in the vault or code.
Never run `npm ci` in the main checkout while agents run: worktrees may share its node_modules. Give each worktree its own `npm ci`.
