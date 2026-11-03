---
name: counterpoints
description: After the owner answers every question in an interview round, research each answer on the web and give the case for and against it, with sources, before the next round starts. Used by kickoff.
---

# Counterpoints

A check on every interview round, so no decision goes into the master plan untested. Run it after the owner has answered every question in a round and before you ask the next one.

## Steps

1. Collect the final decision for each question in the round. If the owner accepted your recommendation, the decision is that recommendation.
2. Research each decision on the web. Use the `agent-reach` skill if it's available (in cloud sessions its Exa search works without installing anything), otherwise WebSearch and WebFetch. Look for evidence, common practice and real examples on both sides, preferring sources close to the product's field. Run searches one after another with short pauses if the search service rate-limits.
3. For each decision, write:
   - **Decision:** the answer as given.
   - **Why we should:** 2–4 points with source links.
   - **Why we shouldn't:** 2–4 points with source links, covering risks, costs and alternatives.
   - **Verdict:** keep, adjust or reconsider, in one line.
4. Save the round to `vault/research/kickoff-round-<n>-counterpoints.md` and show the owner the verdicts, leading with any "adjust" or "reconsider".
5. Ask the owner to confirm or change each decision. Only then record the decisions in the master plan's Decision log and start the next round.

## Rules
- Every decision gets a counterpoint, even obvious ones. Keep each one short and skimmable.
- Cite real links. Never invent a source; say "no good source found" instead.
- Decisions the system plan already settles (stack, guardrails, milestones) only need a counterpoint when this product changes them.
