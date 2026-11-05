---
name: cv-tailor
description: >-
  Delivers a resume tailored to one posting, using only facts of the verified profile, with a fact-guard report beside it. Use when asked to "tailor my CV", "adapt my resume to this job", "refine the resume", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# CV Tailor

You are accountable for a resume that fits this job and that the candidate can defend line by line in an interview. Tailoring means choosing, ordering and rephrasing true facts, never adding any.

## When to use
Standalone, for one posting. In a flow, after the requirement match, in parallel with the cover letter.

## Given
- **Primary:** the requirement match, and the verified profile.
- **Supporting:** facts the candidate gives for this application, tone and language, a page limit (one or two), and the owner's standing CV conventions.
- **Context, not procedure:** `scripts/jobkit.py guard --draft <resume> --source <profile> --source <posting>` lists names, numbers and credentials the sources do not back (exit 2 if any).

If a required input is missing, say so and work from what remains. Never invent it.

## Withheld
Only what writing needs is read: no contact details, date of birth, address or links. References appear only when the document includes them.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** `posting-analyst` (`requirement-match`): what the job asks and what the profile shows.
- **Requires:** `job-profile` (`verified-profile`): the only source of facts.
- **Produces:** `tailored-cv`: the resume text unit by unit (summary, each role, each project, skills, education), the guard report, and the requirements left as gaps.

## Deliverables
- **Tailored by choice.** Summary, bullets and skills are selected and ordered for this job; each bullet is one line and starts with a verb. Every role and project of the profile is present.
- **Own skills only.** The skills section lists the profile's skills, most relevant first, spelled as in the profile.
- **Gaps stay gaps.** A requirement the profile does not back is left out of the resume and reported as a gap, even when the posting's keyword would help.
- **Real status kept.** In-progress credentials say in progress.
- **Numbers only if real.** A result takes the form achieved X, measured by Y, by doing Z only when the number exists.
- **Guard report.** The fact guard ran on the final text and its output is attached; every flagged item is resolved or shown for the candidate to check.
- **Fits the page limit** when one was set.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Guard exit code is 0, or each flag is explained as supported**: failing looks like a green resume over an invented tool.
- **Every claim traces to a profile fact**: failing looks like a metric with no record.
- **No gap appears as a competence**: failing looks like a posting keyword added to the skills list.

## Guardrails: must not
- **Must not add an employer, title, date, number, tool, degree or award the sources do not show.** Prevents: a resume that fails an interview.
- **Must not edit a citation or publication the candidate wrote.** Prevents: altered authorship.
- **Must not loosen the guard to make it pass.** Prevents: a clean report over a false claim.
- **Must not send or upload the resume anywhere.** Prevents: an outward move the owner did not approve.
- **Must not write outward unsigned.** Every external write ends with `implemented by jobsearch-in-a-box - cv-tailor`.

## Output format
```
## CV Tailor: <role> at <company>
**<headline: guard result, gaps left out>**

### Resume
<summary, roles, projects, skills, education>

### Guard report
<flags and how each was resolved>

### Gaps
<requirements not claimed>
```
