# disaster-recovery-in-a-box

Skills:

- [`dr-planner`](skills/dr-planner/SKILL.md): runs the business impact analysis, sets RPO and RTO per service, chooses the recovery strategy and writes the failover and failback runbooks. Produces `dr-plan`.
- [`continuity-standards`](skills/continuity-standards/SKILL.md): maps the plan to ISO 22301, ISO/IEC 27031, ISO/IEC 27001 and the other frameworks that apply, and lists the gaps. Produces `continuity-compliance`.
- [`dr-tester`](skills/dr-tester/SKILL.md): designs recovery exercises and reads their results against the targets. Produces `dr-test-report`.

Rules for the brain live in [`.brain/rules`](.brain/rules): targets come from impact, an untested backup is not a backup, measured recovery beats claimed recovery, standards claims name the clause. Import them under supervision with `python scripts/import-brain.py disaster-recovery-in-a-box` (dry-run), then `--apply`.
