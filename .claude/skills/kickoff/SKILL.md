---
name: kickoff
description: Start a new project. Interview the owner in rounds until nothing is left assumed, then write the master plan every later session builds from.
argument-hint: "One line on what you want to build"
disable-model-invocation: true
---

# Kickoff

Turn a rough idea into `vault/master-plan.md`, the document every later session and agent builds from. Ask as much as it takes. A question asked now is cheaper than a wrong build later.

## 1. Start the board

Run `python3 tools/board.py init "<project name>"`, then `python3 tools/board.py agent planner "Interviewing the owner"`. If the owner gave no name, use a short working title and ask for a real one in round 1.

## 2. Interview

Call the Skill tool with `grilling` and follow it: rounds of numbered questions, each with your recommended answer, so that "yes" accepts it. Look facts up yourself rather than asking.

Seed the design tree with these branches. Skip a branch only when the owner has already settled it.

- **Outcome:** what problem this solves, for whom, and what "it worked" looks like in numbers or behaviour.
- **Users:** who uses it, their skill level, devices, accessibility needs.
- **Scope:** the must-haves for version 1, the nice-to-haves, and what is explicitly out.
- **Features:** for each must-have, the main flow, the edge cases and the failure cases.
- **Data:** what is stored, where, who owns it, privacy and retention.
- **Integrations:** outside services, accounts and API keys needed, and who provides them.
- **Platform and stack:** web, mobile or desktop, languages, frameworks, hosting, budget limits. Recommend one; don't list five.
- **Design direction:** mood, references the owner likes, brand colours, fonts, icon set (default: Tabler icons). Use `design-taste-frontend` to propose a direction for front-end work.
- **Quality bar:** testing standard, performance targets, security needs, browsers and devices to support.
- **Autonomy:** which decisions agents may make alone, which need the owner, and how the owner wants to be told about progress.
- **Done:** what must be true to call version 1 finished, and how it gets deployed.

After each round, append the settled answers to the "Decision log" section of `vault/master-plan.md`, creating it from `vault/templates/master-plan.md` on the first round. If the session ends mid-interview, nothing is lost.

## 3. Write the master plan

When the frontier is empty, fill in every section of `vault/master-plan.md` from the template. Write in plain language. Keep file paths and code out of it, because they go stale.

Then run `python3 tools/board.py phase "Master plan"` and ask the owner to read it and reply "approved" or with changes. Do not move on until they approve.

## 4. Hand off

Once the plan is approved:

1. Run `python3 tools/board.py phase Tickets`.
2. Run `python3 tools/board.py agent planner "Master plan approved" --status done`.
3. Tell the owner the next step is `/to-tickets` on the master plan, followed by `/orchestrate`.
4. If the session is long, call the Skill tool with `handoff` first.
