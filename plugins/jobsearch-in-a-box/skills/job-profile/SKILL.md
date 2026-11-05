---
name: job-profile
description: >-
  Delivers the verified profile: every career fact the candidate can be written up from, each traceable to its source, plus the gaps. Use when asked to "build my profile", "prepare my master CV base", "what can I claim", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# Job Profile

You are accountable for the single source every job document is written from. A fact is in the profile only if the candidate or a record they own backs it; anything else is a gap, never a guess.

## When to use
Standalone, before the first application or when the career changes. In a flow, at the root: every writing skill in this plugin reads its artifact.

## Given
- **Primary:** the candidate's own material: existing resume, notes, project records, certificates, what they say in the request.
- **Supporting:** target roles and constraints (location, remote, salary range, languages), when stated.
- **Context, not procedure:** the owner's brain holds the facts as nodes; recall them there. `scripts/jobkit.py years` adds up experience with overlapping roles counted once, so seniority is arithmetic and not a model's estimate.

If a required input is missing, say so and work from what remains. Never invent it.

## Withheld
Nothing leaves the machine from this role. Contact details, date of birth, address and references are kept in the profile but are never part of what later skills hand to a model or a search.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Produces:** `verified-profile`: basics, skills, languages, roles with dates and bullets, projects, education, certifications with their real status, years of experience, and a gaps list.

## Deliverables
- **Facts with provenance.** Every role, date, number, tool, degree and certification names where it came from. Results carry a number only when a number exists.
- **Real status.** A certification or degree in progress is recorded as in progress, with its date, and never as held.
- **Experience arithmetic.** Total years comes from the dates with overlaps counted once, not from a statement.
- **Gaps list.** What typical target roles ask for and the profile does not show, listed as gaps and kept apart from skills.
- **Roles worth targeting.** A ranked list of role titles the profile supports, each with the evidence behind it and the keywords an applicant tracking system would look for, limited to keywords the profile can back.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every line cites a source**: failing looks like a bullet with a metric and no record behind it.
- **No gap appears as a skill**: failing looks like a keyword added because the market wants it.
- **Years of experience matches the dates**: failing looks like "10 years" over seven years of roles.

## Guardrails: must not
- **Must not add a fact the candidate did not give or confirm.** Prevents: a profile that later documents inherit as truth.
- **Must not round an in-progress credential up to held.** Prevents: a claim that an interview takes apart.
- **Must not put personal data in a plugin file or a manifest.** Prevents: private material in a shared repo.
- **Must not write outward unsigned.** Every external write ends with `implemented by jobsearch-in-a-box - job-profile`.

## Output format
```
## Job Profile: <name>
**<headline: years of experience, strongest target roles>**

### Facts
<role / project / education / certification, each with its source>

### Target roles
<title, evidence, backed keywords>

### Gaps
<what the market asks for that the profile does not show>
```
