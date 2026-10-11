# System plan: AI orchestration kit

Status: draft (kickoff interview in progress)

The master document for the orchestration system itself. Product plans live in `vault/master-plan.md`.

## Decision log
- First product: a personal plant-care app. Shipped = available for A'marri's private use without regular debugging or maintenance.
- Checkpoints: drafts sent at three milestones (features, then design, then final product). Anything that costs money interrupts at any point.
- Failure: dropping 15% or more of the master plan because it can't be built or maintained, or needing debugging every day or two. Must look professional and aesthetic, and last.
- Budget: Claude Max $100/month. Avoid paid APIs and token purchases (not a deal breaker long term). Free APIs are fine.
- Master document lives in the kit's vault folder.
- Build on the existing kit; the plant app is its first real test.
- Roles: PM, coders, reviewer, tester, security and performance checkers, designer, researcher. A second-model auditor is wanted later.
- Done = tests pass and a reviewer agent approves. A'marri signs off only at milestones and paywalls.
- Up to 3 coders at once; revisit when other models join.
- Stuck: 3 attempts total, then the PM, which pings A'marri rather than retrying further.
- Milestone drafts: features (working plain app at a private link), design (styled, with screenshots), final (finished app plus a short usage note). Reply "approved" or changes.
- Usage limit mid-build: PM writes a handoff, pauses, resumes next window without asking.
- Priority order restated: quality, then token saving, then automation.
- Auditor: a fresh-context Claude auditor now; a different model audits at milestones later, after asking A'marri (may need a key).
- Runs in Claude Code with GitHub holding code. A'marri will give Claude a folder on their PC, where the vault (Obsidian) and dashboard stay updated.
- Products ship as installable web apps (PWA). A'marri's phone: Google Pixel 9 (Android), so web push reminders work.
- Accounts: only GitHub today. Default free tiers: Vercel (hosting) and Supabase (database, login). A'marri creates them when a build needs them.
- One standard stack for every product: TypeScript and React. Changes need A'marri's OK.

## Open questions
- None yet beyond Rounds 4 to 8.
