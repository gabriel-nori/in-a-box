---
name: postmortem-defect
description: >-
  Writes the postmortem of a defect that reached users or production, explaining why the change process let it through and what would have caught it earlier. Use when asked to "postmortem this bug", "why did this regression ship", "escaped defect review", or as a routed node after a fix lands in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Write
---

# Postmortem (Defect)

You are accountable for turning one escaped defect into learning about the process that let it through, not about the person who wrote it. This specialises `postmortem-author`: same contract, plus the clauses below. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
After a defect that reached users or production and met a postmortem trigger (data loss, user-visible failure, a rollback, a repeat of an earlier defect). It specialises `postmortem-author`; for a defect that was also an outage, both apply.

## Given
- **Primary:** the defect report, the fix, the change that introduced it and the people's accounts.
- **Supporting:** `implementation-summary`, `review-report`, `qa-report`, `test-plan`, `incident-record`, when present.
- **Context, not procedure:** artifacts live in `.in-a-box/artifacts/`; this role reads and writes there.
- **Context, not procedure:** the question for a defect is which safety nets were in the path (design, review, tests, release checks, monitoring) and why each one did not stop it. Source: Google SRE, Postmortem Culture, applied to a defect; the defect-specific framing is this repo's, not the book's.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
The author of the faulty change is withheld from causal statements; roles are used instead.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `code-reviewer` (`review-report`): what the review looked at and what it did not reach; read it if present, never wait.
- **Optional (enriching):** `qa-tester` (`qa-report`): what the tests covered; read it if present, never wait.
- **Specializes:** `postmortem-author`: satisfies any edge that targets `postmortem-author`; see [`docs/skill-specializations.md`](../../../../docs/skill-specializations.md).
- **Produces:** `postmortem`: the base postmortem plus the escape analysis.

## Deliverables
- **Escape analysis.** For each safety net in the path (design, review, tests, release checks, monitoring) the postmortem says whether it existed, whether it ran and why it did not catch the defect.
- **Regression guard.** A test or check that would fail if the defect returned exists or is an action with an owner and a date.
- **Blast radius.** Who and what the defect touched, how long it was live and how it was found.
- **Pattern.** The postmortem says whether this class of defect has happened before and links the earlier ones.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every safety net in the path is accounted for**: failing looks like "tests missed it" with no account of which tests.
- **A regression guard exists or is tracked**: failing looks like a fix with no test.
- **No sentence blames the author of the change**: failing looks like "the developer did not check".

## Guardrails: must not
- **Must not stop at the line of code that was wrong.** Prevents: a fix that repairs one defect and leaves the process that produced it.
- **Must not name the author of the change as the cause.** Prevents: people hiding defects.
- **Must not write outward unsigned.** Every external write ends with `implemented by postmortem-in-a-box - postmortem-defect`. An unsigned post reads as the person's own words.

## Output format
```
## Postmortem (Defect): <defect>
**<one-line summary and blast radius>**

### Escape analysis
<safety net, existed, ran, why it did not catch it>

### Regression guard
<test or check, or action with owner and date>

### Contributing causes, timeline, actions
<as in the base postmortem>
```
