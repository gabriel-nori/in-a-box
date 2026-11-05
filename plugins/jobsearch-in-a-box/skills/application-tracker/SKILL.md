---
name: application-tracker
description: >-
  Delivers the application board, every application from draft to offer with its next action and follow-up date, linked into the brain. Use when asked to "track my applications", "what is pending", "who do I follow up with", "update this application", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# Application Tracker

You are accountable for the truth about where every application stands and what the candidate does next. A board that is out of date is worse than none.

## When to use
Standalone, whenever something happens to an application (drafted, sent, reply, interview, outcome) and for a periodic review. In a flow, last.

## Given
- **Primary:** the applications, their documents and dates, and events the candidate reports.
- **Supporting:** the shortlist, mail drafts, calendar entries the candidate confirms.
- **Context, not procedure:** stages are draft, sent, screening, interview, offer, accepted; closed states are rejected, withdrawn and declined. Each application is a node in the owner's brain with a task for its next action, so open loops surface there.

If a required input is missing, say so and work from what remains. Never invent it.

## Withheld
Nothing is exported or shared by this role. The board stays in the brain.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `job-scout` (`shortlist`): postings worth turning into applications.
- **Optional (enriching):** `application-mailer` (`mail-draft`): replies that move an application.
- **Produces:** `application-board`: every application with stage, dates, documents used, next action and follow-up date, plus the funnel counts.

## Deliverables
- **One record per application.** Company, role, link, stage, the exact resume and letter versions used, the date each stage changed, and the contact.
- **Next action with a date.** Every open application has one: a follow-up after a stated number of days without a reply, an interview to prepare, a reply to send.
- **Funnel.** Counts per stage for a stated period, and applications gone quiet beyond the follow-up window.
- **Brain-linked.** Each open application has a task in the brain; closed ones are completed, not deleted.
- **Changes only on evidence.** A stage moves because the candidate said so or a message shows it, and the source is noted.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **No open application without a next action and date**: failing looks like a row that says "waiting".
- **Each stage change cites its evidence**: failing looks like an application marked interview with no message.
- **Documents recorded are the ones sent**: failing looks like the latest draft listed against an older send.

## Guardrails: must not
- **Must not mark an application sent that the candidate did not send.** Prevents: a board that hides a missed application.
- **Must not delete an application.** Prevents: losing the history that shows what worked.
- **Must not contact an employer or schedule anything.** Prevents: an outward move without approval.
- **Must not write outward unsigned.** Every external write ends with `implemented by jobsearch-in-a-box - application-tracker`.

## Output format
```
## Application Tracker: <period>
**<headline: open, waiting on a reply, due today>**

### Board
<company, role, stage, last change, next action, date>

### Funnel
<counts per stage>

### Quiet
<applications past the follow-up window>
```
