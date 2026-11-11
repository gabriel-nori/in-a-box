THE RULE

Write the test first and see it fail for the reason you expect. A test that still passes when the code under test returns nothing is worthless and is not counted as evidence.

What must be true at the end:
- Each acceptance criterion has a test that was seen failing before the code existed.
- The implementation summary names that failing run.

How it is handled:
- Small steps: one failing test, the least code that makes it pass, then tidy.
- When a test passes on first run, the test is suspect before the code is trusted.

WHY

A green test run proves nothing if the test could never fail. Seeing red first is the only cheap proof that the test checks the behaviour it names.

HOW TO APPLY

Applies to every developer skill. The summary's Verification section cites the failing run next to the passing one. Where a unit has no testable behaviour (a rename, a config move) the summary says so instead of citing a run.

RELATED

Idea taken from the ub-mode skill (MIT; reached through a short link, https://lnkd.in/dfJ7xq5d; the text is not copied). Roles: developer, quality-gate.
