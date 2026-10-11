---
name: handoff
description: Write a handoff note so the next session can pick up exactly where this one stopped. Use before ending a session, when context is getting long, or when the owner says to wrap up.
argument-hint: "What the next session should focus on (optional)"
---

# Handoff

Sessions start fresh. This note is the only memory the next one gets, and the session-start hook loads the newest one automatically.

Adapted from Matt Pocock's `handoff` (MIT).

Save it to `vault/handoffs/<YYYY-MM-DD-HHMM>-<short-slug>.md` and keep it under 60 lines. Use this structure:

```
# Handoff: <short title>
Date: <date and time> · Phase: <phase from board.py show>

## Goal right now
One or two sentences.

## Done this session
Bullet list of outcomes, not activity.

## Current state
Paste the output of `python3 tools/board.py show --brief`.

## Next steps
Numbered and concrete, in order. The first one should be doable without reading anything else.

## Open questions for the owner
Each with your recommended answer, or "None".

## Pointers
Paths to the plan, tickets, decisions and branches involved. Don't copy their content.

## Suggested skills
The skills the next session should use first.
```

Rules:
- Don't repeat what already lives in the master plan, tickets, decisions or commits. Point to it instead.
- Never include API keys, passwords or personal data.
- If the owner gave a focus, shape "Next steps" around it.
