THE RULE

Hold every change to measured limits, and say "not measured" when a limit could not be measured.

What must be true at the end:
- CRAP score per function is at most 10, where CRAP = CC² × (1 − coverage)³ + CC.
- No two functions are near-duplicates (structural similarity under 0.8).
- Mutation score meets its floor (0.8 by default) when mutation testing ran.
- A check that was not run is reported as not measured, never as passed.

How it is handled:
- The numbers come from `scripts/qualitygate.py` or from a named tool's report, never from reading the code.
- Limits change only through the repo's own config, with the owner's say.

WHY

A number cannot be argued with and a feeling can. A gate that counts the unmeasured as green gives false comfort exactly where coverage is poorest.

HOW TO APPLY

The quality-gate skill applies it after the developers and before the code review. Python is measured natively; other stacks feed in the repo's own tool reports. Kotlin, SQL and IaC are not measured.

RELATED

Measures named after Uncle Bob's crapper, dryer and mutator tools and the ub-mode skill (MIT; reached through a short link, https://lnkd.in/dfJ7xq5d; the repos were read earlier but their URLs were not kept, so the exact defaults of the tools are unconfirmed here). Roles: quality-gate, developer, code-reviewer.
