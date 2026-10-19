# observability-in-a-box

Skills:

- [`observability-engineer`](skills/observability-engineer/SKILL.md): plans and applies logs, metrics, traces, APM wiring, deployment visibility and alerts. Produces `observability-plan`.
- [`observability-reader`](skills/observability-reader/SKILL.md): reads the signals as findings with evidence and confidence. Produces `observability-findings`.

- [`incident-commander`](skills/incident-commander/SKILL.md): runs an incident with one commander, separated roles and a live state document. Produces `incident-record`.

Process: `incident-response` under [`processes`](processes), the one place where order matters. Alerting and SLO standards are brain rules. Postmortems moved to [`postmortem-in-a-box`](../postmortem-in-a-box), because they apply to defects, vulnerabilities and attacks too.

Rules for the brain live in [`.brain/rules`](.brain/rules): how to apply observability, how to alert, log hygiene, how to read signals, service level objectives. Import them under supervision with `python scripts/import-brain.py observability-in-a-box` (dry-run), then `--apply`.
