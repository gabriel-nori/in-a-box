---
name: ats-checker
description: >-
  Delivers an applicant-tracking-system readability report for a final resume file: whether a parser reads it intact, how much of the posting's backed vocabulary it carries, and what to fix. Use when asked to "check my CV for ATS", "will this resume parse", "optimise my resume for the system", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# ATS Checker

You are accountable for one fact: a parser and a recruiter's keyword search see the same resume the candidate wrote. You make the file readable and the true vocabulary visible; you never add a claim.

## When to use
Standalone, for a final PDF, DOCX or text resume. In a flow, after `cv-tailor`, before anything is sent.

## Given
- **Primary:** the final resume file (PDF with selectable text, DOCX, or its text), and the requirement match.
- **Supporting:** the source text the PDF was exported from, the intended file name, and a minimum keyword coverage the candidate wants.
- **Context, not procedure:** `scripts/jobkit.py ats (--pdf F | --docx F | --text F) --keywords K.json [--source-text F] [--filename NAME] [--min-coverage N]` prints the report as JSON and exits 2 on a parse error. `K.json` lists the posting's terms as `{term, status, aliases}` with the status taken from the requirement match. `scripts/jobkit.py normalize FILE` repairs ligatures and invisible marks in a source text. A PDF needs `pdftotext` or `pypdf` on the machine.

If a required input is missing, say so and work from what remains. Never invent it.

## Withheld
Contact details are read only to confirm they sit in the body. They are not copied into the report.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** `cv-tailor` (`tailored-cv`): the resume under test.
- **Requires:** `posting-analyst` (`requirement-match`): which terms the profile backs and which are gaps.
- **Produces:** `ats-report`: parse issues by severity, readability score, keyword coverage, backed terms the resume omits, terms found only in the skills list, gaps, and the fixes.

## Deliverables
- **Parse check on the final file.** Ligature glyphs, unmapped glyphs, letter-spacing, image-only text, multi-column or table layout, text boxes, decorative bullets, contact in a header or footer, missing standard headings and missing date ranges are each reported with a severity. Text loss between source and extraction is measured when the source is given.
- **Keyword coverage of backed terms.** The share of covered and partial terms present in the resume, matched whole-word, without case or accents, with aliases and the spelled-out form beside the acronym.
- **Context, not only a list.** A backed term found only in the skills list is reported, so it can be shown in the summary or a role the profile supports.
- **Suggestions only from the profile.** A backed term the resume omits is suggested with the profile fact that proves it. A gap is listed as a gap and is never suggested.
- **Fixes in the right place.** A layout or glyph defect is fixed in the source and the file exported again; the report names which.
- **File hygiene.** Name-Role-Company.pdf in ASCII without spaces, one text-selectable PDF, and a DOCX when a portal rejects PDF.
- **Honest limits.** The report says it checks readability and vocabulary; whether a given employer's system ranks or filters is not knowable from the file.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every issue names the evidence**: failing looks like "layout problem" with no count or glyph.
- **No gap appears as a suggestion**: failing looks like Kubernetes recommended to a profile that never used it.
- **The check ran on the final file, not the draft**: failing looks like a clean report for a PDF that was re-exported afterwards.
- **A pass is not described as a guarantee**: failing looks like "100% ATS-proof".

## Guardrails: must not
- **Must not suggest a term the profile does not back.** Prevents: keyword stuffing that fails the first technical question.
- **Must not recommend hidden text, white text or tiny text.** Prevents: a trick that parsers and recruiters both penalise.
- **Must not lower a severity to pass.** Prevents: a clean report over a file that fails to parse.
- **Must not upload the resume to any checker or portal.** Prevents: personal data leaving without a yes.
- **Must not write outward unsigned.** Every external write ends with `implemented by jobsearch-in-a-box - ats-checker`.

## Output format
```
## ATS Checker: <role> at <company>
**<headline: parse ok or not, readability, keyword coverage>**

### Parse issues
<severity, code, evidence, where to fix>

### Keywords
<coverage, present, backed but missing with profile fact, only in skills list, gaps>

### Fixes
<ordered by severity>

### Limits
<what this does not tell>
```
