THE RULE

Check a workload design against the quality pillars and record the trade-offs knowingly taken.

What must be true at the end:
- Findings per pillar, risks accepted by name, and actions.

How it is handled:
- AWS names six pillars: operational excellence, security, reliability, performance efficiency, cost optimisation, sustainability. Google Cloud names six: operational excellence, security privacy and compliance, reliability, cost optimisation, performance optimisation, sustainability. Azure lists five pillars (reliability, security, cost optimisation, operational excellence, performance efficiency) and treats sustainability as a workload area.
- Align design choices with the pillar principles, build on the technical design areas, then use the review tools to assess readiness before production.
- Record each trade-off, who accepted it and why.

WHY

Trigger: A design is proposed, before production, or on a planned review.

Inputs:
- The design, the requirements and the constraints.

HOW TO APPLY

Participants: The architect, the workload owner and the engineers.

Expectations of the position:
- **Architect:** names the trade-offs instead of hiding them.

RELATED

Sources (S-017, S-018, S-019): S-017 (primary, pillar list only), S-018 and S-019 (primary, read). The per-pillar design principles were not read.

Roles: solution-architect, architect-aws, architect-azure, architect-gcp. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
