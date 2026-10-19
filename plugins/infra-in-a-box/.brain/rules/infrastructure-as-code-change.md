THE RULE

Change infrastructure through code, reviewed and previewed, with the runtime impact understood.

What must be true at the end:
- A reviewed change, a preview of its effect, an applied and verified result.

How it is handled:
- HashiCorp recommends collaborative infrastructure as code with a shared workflow that manages boundaries between teams, roles and deployment tiers, and a maturity model to assess practice.
- DORA lists the supporting capabilities: version control, deployment automation, continuous integration and delivery, flexible infrastructure, monitoring and observability, database change management.

WHY

Trigger: An environment needs to change.

Inputs:
- The desired state, the current state, the change request.

HOW TO APPLY

Participants: The infra engineer, reviewers and the owner of the environment.

Expectations of the position:
- **Infra engineer:** previews before applying and keeps environments separated.

RELATED

Sources (S-043, S-016): S-043 (primary, overview page only), S-016 (primary, capability list only). Thin: the detailed Terraform and Ansible guidance stays in the specialist skills until it is sourced.

Roles: infra-engineer, infra-terraform, infra-ansible. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
