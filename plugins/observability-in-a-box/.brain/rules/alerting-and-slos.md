THE RULE

Alert on symptoms users feel, against an objective, and make every alert actionable.

- Define a service level objective (an indicator, a target and a window) for each user-facing component; if none is agreed, propose one and mark it proposed.
- Page on symptoms (error rate, latency, availability, burning error budget), not on causes (CPU, a single host down) unless the cause has no other visible symptom in time.
- Every alert carries an owner, a first action (a runbook or an inline note) and the reason it pages rather than notifies.
- Anything that needs no human action in the next day is a ticket or a dashboard, not a page.
- Prefer burn-rate alerts over raw thresholds: one fast window to catch outages, one slow window to catch leaks.

WHY

Cause-based and ownerless alerts train people to ignore pages. Objectives give the team a shared definition of "bad enough", and an action-first alert shortens the time to the first useful step.

HOW TO APPLY

When adding or reviewing an alert, fill the four fields (detects, owner, first action, why it pages). Delete or demote any alert that cannot fill them. Review alert quality after each incident: which alerts fired, which were useful, which were silent when they should not have been. Changes to paging or retention in production wait for a human gate.

EXCEPTIONS

Hard safety limits (disk full, certificate expiry within days, quota exhaustion) may alert on a cause because the symptom arrives too late.

JUDGED AGAINST

Every alert in the plan has owner, first action and page reason; user-facing components have an objective or a proposed one; no alert is a bare threshold with no context.

RELATED

observability-apply-signals; observability-read-signals
