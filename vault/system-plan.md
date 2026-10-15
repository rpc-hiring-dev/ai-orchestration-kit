# System plan: AI orchestration kit

Status: approved on 2026-10-11

The master document for the orchestration system itself. Each product gets its own plan in `vault/master-plan.md` through `/kickoff`.

## 1. Vision and definition of done
A personal agent team that turns one interview into a shipped product with little babysitting. Priorities in order: quality and consistency, token savings, autonomy, visibility.

The system is done when the plant-care app ships through it: A'marri uses it privately on their Pixel 9 without regular debugging, all three milestone drafts were delivered, and the build never needed a check-in outside milestones, money or a stuck agent.

It has failed if 15% or more of a master plan is dropped because it can't be built or maintained, if a product needs debugging every day or two, or if the output looks unprofessional or inconsistent.

## 2. Decisions log
See "Decision log" at the end of this file. Every answer and accepted default is there, one line each.

## 3. System architecture
**Flow:** A'marri gives an idea, then `/kickoff` interviews them and writes the product's master plan. They approve it. `/to-tickets` splits it into tickets. `/orchestrate` turns the session into the PM, which runs the build until done.

**Roles**
- **PM:** plans, hands out tickets, merges reviewed work, keeps the board current, writes the session handoff. Writes no product code.
- **Researcher:** looks up library docs and approaches before a ticket starts and leaves a short note coders read instead of browsing.
- **Designer:** sets the product's design system at the design milestone using the design skills, GSAP and React Bits.
- **Coders (up to 3 at once):** one ticket each, test-first, report to the PM in 10 lines or fewer.
- **Reviewer, tester, security and performance checkers:** check every ticket before merge (security only when it touches login, input or personal data).
- **Auditor:** a fresh-context Claude that sees only the plan and the finished work, at each milestone. A second model can join later at milestones only, after A'marri's OK.

**Task done** = tests pass and the reviewer approves.
**Stuck** = 3 attempts in total, then the PM, which alerts A'marri instead of retrying.
**Usage limit** = the PM writes a handoff, pauses and resumes in the next window on its own.

**Milestones A'marri signs off:** features (a working plain app at a private link), design (fully styled, with screenshots), final (finished app plus a short how-to). They reply "approved" or list changes.

## 4. Tool stack
| Tool | How it's connected | Token cost |
|---|---|---|
| Kit skills (Pocock, Osmani, design-taste) | Copied skills, loaded only when called | Low: only names load until used |
| GitHub | Already connected | Low |
| Claude Code in this project | Where agents run, covered by Max | Uses plan usage |
| Browser checks | Built in; screenshots and click-through tests | Medium per run, so used at review time only |
| Vercel (hosting), Supabase (database, login) | Free tiers, connected inside each product repo only | None in other sessions |
| GSAP | Installed from npm per product | None until used |
| React Bits | Individual components copied in as needed | Low |
| Alerts | A private Telegram bot (free), with Resend email as an option | None |
| Obsidian | Opens the vault in A'marri's PC folder | None |
Per-project later: graphify, watermelon-platform, bklit-ui. Motion is dropped in favour of GSAP. Parked links stay in "Parked tools".

## 5. Dashboard spec
Lives as a browser page and the Obsidian Dashboard note in A'marri's PC folder, plus the live thread status in the project. It shows:
- each agent's task, status, last update and blocker;
- the current milestone and overall percent complete;
- token use, estimated and actual, per ticket and in total;
- build screenshots over time, shown as a before-to-after transformation timeline.

Alerts go by Telegram push (or email) only for milestone drafts, anything that costs money, stuck agents and the usage check-in. Nothing for routine progress. Contacts are kept with each product, never in the kit or memory.

## 6. Handoff template and rules
- The PM writes one handoff per session, under 60 lines, in the product's vault. It auto-loads next session.
- Coders never write handoffs; they report to the PM in 10 lines or fewer.
- Kept: decisions, conventions, ticket status, open questions. Dropped: chat history and dead ends.
- Template: goal right now, done this session, board state, next steps, open questions with recommended answers, pointers, suggested skills (already in the kit's handoff skill).

## 7. Quality rules
- Every agent follows the kit's code review and design skills and the product's design system.
- Each product has a short conventions note (naming, structure, design tokens) that every agent reads first; the reviewer rejects work that breaks it.
- One stack for every product: TypeScript and React. Changing it needs A'marri.
- Before a ticket is done: automated tests for logic, a click-through test of each main flow, and a screenshot check at phone size.

## 8. Guardrails
Need A'marri's approval: spending money, making anything public, deleting data, repos or accounts, adding an outside service or key, changing the stack, changing the kit itself, and continuing past half the week's Max usage (A'marri names the percent).
Agents may do alone: merge reviewed work, update private preview links, make choices the master plan's autonomy rules allow (logged in `vault/decisions/`).
No deadlines. Agents work and send alerts any time.

## 9. Build order
1. **Update the kit:** add researcher, designer and auditor agents; set the 3-attempt rule, milestone drafts, usage check-in and guardrails in `/orchestrate`; add the conventions note; add token use and screenshot timeline to the board and dashboard. Milestone: a dry run on a tiny sample app passes end to end.
2. **Connect A'marri's side:** the PC folder for the vault and dashboard, and the free email service for alerts. Milestone: a test alert email arrives and the dashboard opens in Obsidian.
3. **Plant app kickoff:** a new repo from the kit and its own `/kickoff` interview. Milestone: its master plan is approved.
4. **Plant app build:** tickets and orchestration through the features, design and final drafts. Milestone: final draft approved and in daily use.
5. **Retro:** the PM proposes kit changes from what went wrong. Milestone: A'marri approves or declines each.

## 10. Open questions
None. Settled on approval:
- Agents can't read the Max usage meter, so the PM estimates tokens against a weekly budget and asks A'marri to confirm the real figure at the check-in.
- Alerts use a free Telegram bot (chosen 2026-10-11). Resend's free tier was tried first and only delivers to its own account address; ntfy's free quota is shared per cloud IP.
- The kit becomes a GitHub template repo.

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
- Alerts by Telegram push for now (free), email optional; no paid texts.
- GSAP is the one animation library; Motion is dropped.
- Survives between sessions: decisions, conventions, ticket status, open questions. Chat history and dead ends are forgotten. Reassess later if needed.
- Handoffs live in each product's vault (synced to the PC folder). Max 60 lines. Coders report to the PM in 10 lines or fewer; only the PM writes the session handoff.
- Standards: the kit's code review and design skills, plus one design system per product set at the design milestone.
- Done requires automated tests for logic, a click-through test of each main flow, and a phone-size screenshot check.
- Consistency: a short conventions note per product that every agent reads first; the reviewer rejects work that breaks it.
- Guardrails: never without approval: spend money, make anything public, delete data, repos or accounts, add a new outside service or key, change the standard stack. Agents may merge reviewed work and update private preview links.
- No deadlines; quality over speed.
- Builds may use about half the weekly Max usage. At that point the PM asks A'marri whether to continue and up to what percent, instead of pausing on its own.
- Agents work and send alerts any time.
- After each product the PM proposes kit changes; A'marri approves before they're made.
- Plant app data is private: only A'marri can sign in, nothing is shared, export or delete any time.
