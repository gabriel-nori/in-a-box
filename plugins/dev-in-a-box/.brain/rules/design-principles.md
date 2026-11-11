THE RULE

Before writing code, test the premise, then prefer the smaller change: the least code that solves the real problem, behind clear boundaries.

What must be true at the end:
- The root cause is addressed, not the symptom.
- Operations that can run twice are safe to run twice (idempotent).
- Each boundary (module, service, input) validates what crosses it and trusts nothing beyond it.
- Code that was not needed was not written.

How it is handled:
- Challenge the request's premise first: is this the problem, or a symptom of it?
- Be lazy on purpose: reuse what exists, delete before adding, stop at the requirement.
- Fix the cause and say what was the cause; a patch over a symptom is reported as one.

WHY

Most defects and most rework come from solving the wrong problem or from code that did not need to exist. These habits are cheap at the start and expensive to retrofit.

HOW TO APPLY

Applies to developers and the tech lead when slicing work. A unit that keeps a premise it could not verify says so in the implementation summary.

RELATED

Ideas taken from the ub-mode skill (MIT; reached through a short link, https://lnkd.in/dfJ7xq5d; the text is not copied). Roles: developer, tech-lead.
