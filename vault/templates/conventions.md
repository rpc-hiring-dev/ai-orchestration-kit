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

## Data and privacy
- Privacy is enforced in the database (row-level security on every table), not only in the screens.
- Every access rule checks the person's role (e.g. `my_role()`), never just "signed in", so switching someone off takes effect at once.
- Columns some users must not see (door codes, phone numbers, notes) live in their own table or behind a view, never hidden by row rules alone.
- Schema changes are migration files, tested on a local copy. Production runs them only with the owner's OK.

## Design
Points to `vault/design-system.md` once the designer writes it. Icons: Tabler. Animation: GSAP only.

## Copy
Plain language, short sentences, no jargon. Errors say what happened and what to do next. Sentence case for labels and buttons.

## Testing
Automated tests for logic, a click-through test of each main flow, and a screenshot check at phone size before a ticket is done.
Run e2e with a unique `PW_PORT` (e.g. 4100 + ticket number) when other agents may be running tests; the e2e config reads it.
Lint and test configs ignore `.claude/worktrees/`.
Tests that create databases, files or ports use unique, always-cleaned-up names, so parallel agents don't collide.
An automated accessibility scan (e.g. `@axe-core/playwright`, WCAG 2.2 AA) runs on every screen in the browser tests, for each role, at phone and desktop size.
Never run `npm ci` in the main checkout while agents run: worktrees may share its node_modules. Give each worktree its own `npm ci`.

## Test data
Every seed and test row is marked (for example `source = 'seed'` or an id prefix) so go-live removes them in one step. Settings that choose a data source default to the live source in production; fixtures are for tests only.

## AI features
Any feature that calls a model (ask a question, summarise, check a listing) starts with cost and scope limits:
- It answers only from data the person can already see on screen or through their access rules, and refuses off-topic questions in one line.
- Easy questions go to the cheapest model that handles them; only hard ones go to a larger model. Cache the fixed instructions.
- A monthly spend cap, checked before each call, with an email to the owner when it is reached (the cap amount is the owner's call).
- A question log (who, when, model, cost; never more personal data than needed), deleted after 90 days.

## Secrets
Keys and contact details go in `.env`, never in the vault or code.
