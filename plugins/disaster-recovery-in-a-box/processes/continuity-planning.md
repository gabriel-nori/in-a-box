---
id: continuity-planning
title: Contingency and continuity planning
scenario: business impact analysis, bia, contingency plan, continuity plan, maximum tolerable downtime, recovery objectives
roles: [dr-planner, continuity-standards]
sources: [S-024, S-023, S-025]
---

# Contingency and continuity planning

## Purpose
Derive recovery priorities and targets from the business, then plan, test and maintain recovery.

## Trigger
A system or service is introduced, changes materially, or a plan is due for review.

## Participants
System owners, the DR planner, business owners and management.

## Inputs
- A contingency policy, the system's business functions and dependencies.

## Outcomes
- Maximum tolerable downtime, RTO and RPO from a business impact analysis, preventive controls, recovery strategies, a contingency plan, a test, training and exercise plan, and maintenance.

## How it is handled
- The NIST process has seven steps: develop the contingency policy statement, conduct the business impact analysis, identify preventive controls, create recovery strategies, develop the contingency plan, plan testing, training and exercises, and plan maintenance.
- The business impact analysis supplies the maximum tolerable downtime, RTO and RPO that drive every recovery decision.
- ISO 22301 expects traceability: BIA targets, strategies, plans and exercise evidence tie to each other.

## Expectations of the position
- **DR planner:** keeps the chain traceable. **Business owners:** own the impact numbers.

## Sources
S-024 (secondary, search summary) for the seven steps. S-023 (primary) confirms the publication and its scope but its body was not read. S-025 (secondary) for ISO 22301. Treat step names as reliable and details as to be checked against SP 800-34 Rev. 1.
