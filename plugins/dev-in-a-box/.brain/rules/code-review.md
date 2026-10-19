THE RULE

Make sure the change improves the overall health of the codebase, and get it merged without needless delay.

What must be true at the end:
- A decision to approve, approve with comments or request changes, with reasons.
- Optional suggestions marked `Nit:`.

How it is handled:
- Approve once the change clearly improves code health, even if it is not perfect; do not approve a change that worsens it, except in an emergency.
- Judge on maintainability, consistency and the other aspects; style follows the style guide, design follows engineering principles and data, not preference.
- Resolve disagreements by seeking consensus first (a conversation, with its outcome written on the change), then escalate to a team discussion, tech lead, maintainer or manager. A change does not stall on disagreement.

WHY

Trigger: A change is ready for review: small, described and tested by its author.

Inputs:
- The change and its description.
- The repo's style guide and conventions.

HOW TO APPLY

Participants: The author and one or more reviewers; a tech lead or code owner for escalation.

Expectations of the position:
- **Reviewer:** reviews promptly, is specific, and rests blocking comments on principles.
- **Author:** keeps changes small, writes a good description, answers reviewer comments.

RELATED

Sources (S-011, S-012): S-011 (primary, read in full). S-012 (primary, index page only; the sub-guides on small changes, descriptions and handling comments were not read).

Roles: code-reviewer, tech-lead, developer. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
