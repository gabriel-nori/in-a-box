---
id: blameless-postmortem
title: Blameless postmortem
scenario: postmortem, post-mortem, RCA, root cause analysis, lessons learned, incident review, bug postmortem, security incident review, breach review, vulnerability review
roles: [postmortem-author, postmortem-defect, postmortem-security, incident-commander]
sources: [S-006, S-062]
---

# Blameless postmortem

## Purpose
Learn from an incident, an escaped defect, a vulnerability or an attack by explaining its contributing causes and fixing the system, without blame. The order matters because the draft needs the record, the review needs the draft, and the actions need the review.

## Trigger
A trigger defined before incidents occur: user-visible downtime beyond a threshold, any data loss, on-call intervention such as a rollback, resolution time above a threshold, or a monitoring failure that forced manual discovery. Any stakeholder may also request one. The same trigger logic applies to a defect that reached users and to a security event; the specialist skill adds the escape analysis or the exposure analysis.

## Participants
The people involved in the incident, senior engineers who review the draft, and the stakeholders who receive the outcome.

## Inputs
- The incident record, timeline, logs and the participants' accounts.

## Outcomes
- A postmortem with impact, mitigation, causes and follow-up actions; actions tracked to completion; the postmortem stored where other teams can find it.

## How it is handled
- Focus on contributing causes, not on individuals or teams; assume good faith with the information people had.
- Write: incident record and impact, actions taken, root causes, follow-up actions.
- Review a first draft with senior engineers for key data, impact, depth of root cause, an appropriate action plan and sharing of the outcome.
- Prioritise and complete the actions; aggregate postmortems to spot cross-team trends.
- Share widely, removing end-user identifying information.

## Expectations of the position
- **Author:** writes in terms of systems and roles. **Reviewers:** challenge the depth of the analysis. **Owners of actions:** deliver them.

## Sources
S-006 (primary, read in full). The extension to defects and security events is this repo's application of the same standard; the book describes incidents only. NIST SP 800-61 Rev. 3 (S-062) is cited for the security case by publication record only. The Google text does not describe tracking tools; the choice of tracker is the team's.
