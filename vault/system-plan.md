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
- New design resources: GSAP (animation library, free; install from npm per product) and React Bits (copy individual animated components per product, not the whole pack).
- Vercel and Supabase connect per product repo only. Agents check visuals with a browser (screenshots and click-through tests). Only the researcher looks up library docs; coders read its notes.
- Dashboard: browser page and Obsidian note in A'marri's PC folder, plus live thread status. Shows each agent's task, status, last update, blocker, current milestone, percent complete, token usage (estimated and actual), and build screenshots over time as a before-to-after transformation view.
- Alerts only for milestone drafts, money, and stuck agents: Claude app push, plus email or text per product. Contacts are kept with each product, never in the kit or memory.
- Alerts by email only for now (free); no paid texts.
- GSAP is the one animation library; Motion is dropped.
- Survives between sessions: decisions, conventions, ticket status, open questions. Chat history and dead ends are forgotten. Reassess later if needed.
- Handoffs live in each product's vault (synced to the PC folder). Max 60 lines. Coders report to the PM in 10 lines or fewer; only the PM writes the session handoff.
- Standards: the kit's code review and design skills, plus one design system per product set at the design milestone.
- Done requires automated tests for logic, a click-through test of each main flow, and a phone-size screenshot check.
- Consistency: a short conventions note per product that every agent reads first; the reviewer rejects work that breaks it.

## Open questions
- None yet beyond Rounds 4 to 8.
