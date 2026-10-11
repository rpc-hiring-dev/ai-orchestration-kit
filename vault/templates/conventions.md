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

## Secrets
Keys and contact details go in `.env`, never in the vault or code.
