---
id: incident-response
title: Incident response
scenario: incident, we are down, outage, declare an incident, incident commander, on-call escalation
roles: [incident-commander, observability-reader, infra-engineer]
sources: [S-005]
---

# Incident response

## Purpose
Restore service quickly while keeping a coordinated response and a record good enough to learn from.

## Trigger
Declare early: a second team is needed, customers can see the outage, or the problem is unsolved after about an hour of focused analysis.

## Participants
Incident command, operations lead, communications, planning; one person may hold several roles in a small team, except command and operations.

## Inputs
- The alert or report, the available responders, dashboards and runbooks.

## Outcomes
- Service restored and verified, a live state document, an incident record, follow-up actions.

## How it is handled
- Incident command holds the high-level state, organises the team, assigns work by need and priority and removes roadblocks; command holds any role it has not delegated.
- Operations is the only group changing the system.
- Communications sends periodic updates and keeps the state document accurate.
- Planning files bugs, arranges hand-offs and logistics, and tracks how the system has drifted from normal.
- Keep one live state document with the most important facts at the top; use one known coordination place.
- Hand off by briefing fully, transferring command explicitly and waiting for acknowledgement.
- When the load is too heavy, ask planning for more staff and delegate, or open sub-incidents.

## Expectations of the position
- **Incident commander:** decides and delegates; does not operate.
- **Operations lead:** the only one who changes the system.
- **Communications lead:** keeps everyone informed on a cadence.

## Sources
S-005 (primary, read in full). Severity scales and paging policy are organisation-specific and not sourced here; the Atlassian handbook could not be read.
