---
name: feature
description: Make one change to a product after a draft or after launch. One thread per change - research, a branch, a pull request with before-and-after screenshots, the owner's OK to merge, then each live step with its own OK.
argument-hint: "What to change, in the owner's words"
disable-model-invocation: true
---

# Feature

After the first draft, most work is a stream of small requests: "add a role", "email the office when a task changes", "make the property page tabs". Each one gets its own thread and runs through this skill, start to finish. The PWS build ran more than twenty changes this way after launch.

## 1. Get oriented (cheaply)

1. Read the project memory summary (or the newest handoff if there is no shared memory), `vault/conventions.md`, `vault/design-system.md` and `vault/setup-traps.md`. Read only the parts of `vault/master-plan.md` and the code this change touches.
2. Write down, in one line each, what the owner asked for and what you will build. If the ask can be read two ways, take the likelier one and say which you chose.

## 2. Decide before you build

- Look up facts yourself (how the code works today, what the provider allows, what similar apps do). Use the `researcher` agent for anything outside the codebase.
- If the change has a real choice the owner would care about (who can see it, wording people will read, a layout), put the options to them **once**, with your recommendation. For anything they will look at, send screenshots or mockups to pick from, labelled A, B, C, rather than a description. Keep building the recommended option while they decide, unless it can't be undone.
- Anything on the guardrail list (money, a new outside service or key, deleting data, making something public) waits for the owner's OK.

## 3. Build

1. Branch from `main` (or, in a cloud session, use the session's branch based on the latest `main`).
2. Follow `vault/conventions.md`. Test first for logic; add or extend a click-through test for the flow. Write database changes as a new migration file and test them against a local copy, never against production.
3. Run the type checker, linter and full test suite. Start `code-reviewer` on the branch, and `security-auditor` too if the change touches sign-in, who can see what, user input or personal data. Fix what they flag.
4. Take screenshots of every screen the change touches, **before and after**, at phone and desktop size (light and dark if the app has both). Save them in `vault/screenshots/<date>-<slug>-<screen>-<before|after>-<phone|desktop>.png`, and in the project's shared folder when there is one, so the owner can see them without opening the repo.

## 4. Pull request

Open one pull request per change. Its description says, in plain words:
- what changed for each kind of user;
- the screenshots (or where they are);
- **what going live needs**, as a list: each migration, function deploy, secret, setting, scheduled job or switch-on, and who does it.

Nothing is merged without the owner's OK. When they say so, merge it.

## 5. Go live, one step at a time

Follow the "Live changes" rule in `CLAUDE.md`: each live step (migration on production, function deploy, secret, switching on emails, schedules or webhooks) happens only with the owner's OK for that change. The OK to merge covers the live steps only when the owner says so, or the pull request's "what going live needs" list was in front of them when they said it.

Then check it worked on the live app, and reply with a short **What went live** list: each step, done or waiting, and anything the owner has to do (with the exact setting name or link).

## 6. Record it

- One line in `vault/decisions/<date>-<slug>.md`: what was decided and who decided it.
- One line in project memory, in the form described in `vault/project-memory.md`: the feature, PR number, its state (PR open, merged, LIVE), the date and who gave the OK. Update that line as the state changes; don't add a second one.
- Any new setup trap goes into `vault/setup-traps.md`.
- If the change alters what users do, update the role guide it affects (see "Role guides" in `/orchestrate`).

The thread is finished when the change is live and checked, or the owner has said to stop.
