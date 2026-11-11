THE RULE

Commit in small steps, in the order a reader needs them, and let each commit carry its reason, its change and its proof.

What must be true at the end:
- Each commit does one thing and leaves the build and tests passing.
- The message says why first, then what, then how it was verified.
- Unrelated changes are in separate commits.

How it is handled:
- Split a large change along its seams before committing, not after review asks.
- A commit that needs "and" in its subject is two commits.

WHY

Small ordered commits make review faster and make a bad change revertable alone. A commit message that says why survives the code it describes.

HOW TO APPLY

Applies to every developer skill on its branch. It never licenses a push to the default branch or an unsigned outward write; those stay guardrails of the skill.

RELATED

Idea taken from the ub-mode skill (MIT; reached through a short link, https://lnkd.in/dfJ7xq5d; the text is not copied). Roles: developer.
