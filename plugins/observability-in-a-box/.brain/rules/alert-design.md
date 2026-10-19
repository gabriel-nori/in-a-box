THE RULE

Page a human only for what is urgent, actionable and needs judgement, and keep the cause-level detail for debugging.

What must be true at the end:
- Alerts that each have an owner and a first action, and a lower rate of noise.

How it is handled:
- Measure at least latency, traffic, errors and saturation for user-facing systems.
- Page on symptoms (what users feel); keep causes (what is overloaded) for diagnosis.
- Keep rules simple. A page a script could handle is fixed at the root or automated.
- Noisy or robotic alerts cause fatigue; remove or fix them.

WHY

Trigger: A service gains or changes alerts, or on-call load is too high.

Inputs:
- The service's golden signals and its objectives; the history of pages.

HOW TO APPLY

Participants: The observability engineer and the on-call owners.

Expectations of the position:
- **Observability engineer:** owns the quality of the alert set. **On-call:** reports pages that were not actionable.

RELATED

Sources (S-007): S-007 (primary, read).

Roles: observability-engineer. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
