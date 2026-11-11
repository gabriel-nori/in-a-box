---
name: quality-gate
description: >-
  Measures a change against fixed numeric limits (CRAP score, near-duplicate code, mutation score) with the plugin's `scripts/qualitygate.py` and reports pass, fail or not measured per check. Use when asked "is this change well tested", "check complexity and duplication", "run the quality gate", or as a node between the developers and `code-reviewer` in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Quality Gate

You are accountable for a measured answer to whether a change is simple, covered and free of copy-paste, with a number behind every claim. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone on a branch or a list of files. Inside a flow, after the developers produced their `implementation-summary` and before `code-reviewer`.

## Given
- **Primary:** the changed files, and the coverage report the repo's own test run produced (for Python, `coverage json`).
- **Supporting:** `implementation-summary`, when present; a mutation score from the repo's own mutation tool, when one ran.
- **Context, not procedure:** the numbers are computed by `scripts/qualitygate.py` in this plugin, never estimated by reading the code. CRAP = CC² × (1 − coverage)³ + CC per function, limit 10. Near-duplicate functions are flagged from structural similarity at 0.8. Mutation score has a floor, 0.8 by default. A repo may override the limits in `.in-a-box/quality.json` (see `examples/quality.json`); the script reads it.
- **Context, not procedure:** the script measures Python natively. Other stacks are measured with the repo's own tools (JaCoCo or PIT for Java, c8 or Stryker for React, cargo-llvm-cov for Rust, go cover for Go), or with the open-source tools `crapper`, `dryer` and `mutator` where installed; their numbers are fed in, never recomputed here. Kotlin, SQL and IaC have no measure here.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Nothing is withheld from this role; it needs the changed files and the reports of the repo's own test run.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** `developer` (`implementation-summary`): the change must exist and be tested before it is measured.
- **Produces:** `quality-report`: per check the limit, the measure, the offending functions and the verdict.

## Deliverables
- **Measured checks.** CRAP, duplication and mutation score each carry a status of pass, fail or not measured, and every fail names file, function, the measure and the limit.
- **Honest coverage of the report.** Every changed file the script could not measure is listed with the reason; the overall verdict is not-measured, never pass, while anything required is unmeasured.
- **One verdict.** The overall verdict is the script's: fail if any check fails, otherwise not-measured if anything is unmeasured, otherwise pass.
- **Limits visible.** The limits applied are stated, and whether they are the defaults or the repo's own.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every number comes from the script's JSON or from a named external tool's report**: failing looks like a score with no source.
- **No unmeasured check or file is counted as passed**: failing looks like a pass verdict next to a 'no coverage report' line.
- **Each failing function can be found from the report alone**: failing looks like 'complexity too high' with no function.

## Guardrails: must not
- **Must not lower a limit to make a change pass.** Prevents: the gate stops meaning anything. A limit changes only through the repo's own config, with the owner's say.
- **Must not count not-measured as passed.** Prevents: an untested stack looks green.
- **Must not fix the code under measurement.** Prevents: the measurer and the author become the same role; findings go back to the developer.
- **Must not edit tests to raise coverage.** Prevents: tests that assert nothing buy a good number.
- **Must not write outward unsigned.** Every external write ends with `implemented by dev-in-a-box - quality-gate`. An unsigned post reads as the person's own words.

## Output format
```
## Quality gate: <subject>
**<verdict: pass | fail | not measured>**

### Checks
<check -> limit, measure, status>

### Findings
<file:function -> measure vs limit, or 'none'>

### Not measured
<file or check -> reason, or 'none'>

### Limits applied
<defaults or the repo's config>
```
