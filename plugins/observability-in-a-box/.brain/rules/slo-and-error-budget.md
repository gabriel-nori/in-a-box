THE RULE

Agree how reliable a service must be, measure it from the user's side, and say in advance what happens when the budget is spent.

What must be true at the end:
- SLIs, SLOs over a window, an error budget and an error budget policy with owners and an escalation path.

How it is handled:
- An SLI is the ratio of good events to total events, from the user's perspective; separate the specification (what matters) from the implementation (how it is measured).
- An SLO is a target for an SLI over a window, below 100% because perfect reliability is unattainable and would stop necessary change.
- The error budget is 100% minus the SLO.
- Product confirms the threshold is acceptable to users; developers agree to reduce risk when the budget runs out; the operating team confirms the target is reachable without excess toil.
- The policy names owners and actions (prioritise reliability fixes, pause launches, freeze changes) and an escalation path for disagreement.

WHY

Trigger: A user-facing service is defined, or changes, or its reliability is in dispute.

Inputs:
- User journeys and what users notice, current measurements, business tolerance.

HOW TO APPLY

Participants: Product, development and the team operating the service.

Expectations of the position:
- **Observability engineer:** proposes measurable SLIs and instruments them.
- **Product, development, operations:** all three approve the policy.

RELATED

Sources (S-009, S-030): S-009 (primary, read). S-030 (primary, read) for the user-perspective definitions.

Roles: observability-engineer, observability-reader. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
