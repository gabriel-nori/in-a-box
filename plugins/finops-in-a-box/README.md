# finops-in-a-box

Skills:

- [`cost-estimator`](skills/cost-estimator/SKILL.md): prices an architecture from provider pricing sources, with assumptions, ranges and commitment scenarios. Produces `cost-estimate`.
- [`budget-planner`](skills/budget-planner/SKILL.md): sizes a budget from scope and complexity and defines the budgets, thresholds and alerts to apply. Produces `budget-plan`.
- [`cost-monitor`](skills/cost-monitor/SKILL.md): reads actual spend against estimate and budget, finds anomalies, unallocated spend and savings. Produces `cost-findings`.

Rules for the brain live in [`.brain/rules`](.brain/rules): estimate with sources, budgets need owners, tag before you spend, read costs by driver. Import them under supervision with `python scripts/import-brain.py finops-in-a-box` (dry-run), then `--apply`.
