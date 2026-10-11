# Third-party content

These files were copied on 2026-10-11 from the commits listed below. They are pinned copies, so nothing updates on its own. To update one, re-copy it on purpose and review the diff.

| Source | Commit | Licence | Files here | Changes |
|---|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | `49dd158d1076` | MIT | `.claude/skills/{grill-me,grilling,to-questionnaire,to-spec,to-tickets}` | `to-spec` and `to-tickets` write to `vault/` instead of a tracker set up by `/setup-matt-pocock-skills`, and `to-tickets` registers tickets on the board. `handoff` and `implement-spec` were rewritten as our own `handoff` and `orchestrate` skills. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `1be8e34187e3` | MIT | `.claude/skills/{planning-and-task-breakdown,incremental-implementation,test-driven-development,code-review-and-quality,security-and-hardening,shipping-and-launch}`, `.claude/agents/{code-reviewer,security-auditor,test-engineer,web-performance-auditor}.md` | Removed links to the source repo's `docs/agents.md`. |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `717446e07a78` | MIT | `.claude/skills/design-taste-frontend` | None. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `9b58c1ffb790` | MIT | Rules folded into `.claude/agents/coder.md` | Only the coding rules were kept, so they apply to coder agents rather than every session. |

Each project keeps its own copyright notice and MIT licence text in its repository.
