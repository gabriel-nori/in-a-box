# dev-in-a-box

Role: **Developer**. Takes a requirement from spec to implemented code, through a tech lead and stack specialists.

| Skill | What it is | Produces |
|---|---|---|
| [`spec-analyst`](skills/spec-analyst/SKILL.md) | Evaluates the product definition, resolves gaps, writes acceptance criteria, test plan and technical spec | `technical-spec`, `test-plan` |
| [`tech-lead`](skills/tech-lead/SKILL.md) | Default entry to the dev flow. Slices the spec, routes units to specialists, fixes the contracts between them, takes rejected work back | `interface-contracts`, `work-plan` |
| [`developer`](skills/developer/SKILL.md) | Generic implementer, the shared contract of every specialist and the fallback route | `implementation-summary` |
| [`developer-python`](skills/developer-python/SKILL.md) | Specialist: Python | `implementation-summary` |
| [`developer-java`](skills/developer-java/SKILL.md) | Specialist: Java / JVM | `implementation-summary` |
| [`developer-android`](skills/developer-android/SKILL.md) | Specialist: Android | `implementation-summary` |
| [`developer-react`](skills/developer-react/SKILL.md) | Specialist: React | `implementation-summary` |
| [`developer-sql`](skills/developer-sql/SKILL.md) | Specialist: SQL, consults `dba` | `implementation-summary` |
| [`code-reviewer`](skills/code-reviewer/SKILL.md) | Reviews a change for code health; hands each stack to its own reviewer and merges the reports | `review-report` |
| `code-reviewer-python`, `-java`, `-android`, `-react`, `-sql`, `-iac` | One reviewer per stack, each specialising `code-reviewer`; each can call auxiliary reviewers (SQL in any stack goes to `code-reviewer-sql`, which calls `dba`) | `review-report` |

## Customising

- **Routing:** drop a `.in-a-box/routing.yaml` in the workspace; see [`examples/routing.yaml`](examples/routing.yaml).
- **Your own tech lead:** any skill that produces `interface-contracts` and `work-plan` can take the `tech-lead` slot in a flow.
- **A new stack:** add `developer-<stack>` as a specialisation of `developer` (see `docs/skill-specializations.md`).
