---
id: release-rollout
title: Release and rollout
scenario: release, ship, cut a release, version number, canary, staged rollout, rollback plan
roles: [release-manager, changelog-keeper, qa-tester]
sources: [S-008, S-013, S-014]
---

# Release and rollout

## Purpose
Deliver a verified change reproducibly, with the right version number, in stages that can be halted, and with a way back.

## Trigger
A change set has passed review, QA and acceptance and is proposed for release.

## Participants
Release owner, developers, SRE or operations, and the approver of the ship gate.

## Inputs
- The change set and its tests, the changelog, the target environments.

## Outcomes
- A release plan, a version number, release notes, and an approved gate.

## How it is handled
- Releases are self-service and automated; builds are hermetic so the same revision gives the same output.
- Approvals, releases and deployments are gated by review and access control.
- Releases are frequent, so each carries few changes.
- Version with SemVer: MAJOR for incompatible API changes, MINOR for compatible features and deprecations, PATCH for compatible fixes; deprecate in a MINOR release and remove only in a later MAJOR.
- Release notes group changes as Added, Changed, Deprecated, Removed, Fixed, Security, newest first, with dates.
- Use canary releases, staged rollouts and a rollback path; join the project early, since retrofitting is costly.

## Expectations of the position
- **Release manager:** designs and enforces the practice. **Approver:** decides at the gate.

## Sources
S-008, S-013, S-014 (all primary, read). The Google text describes Google's practice; scale-specific parts are not copied.
