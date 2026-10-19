---
id: threat-modeling
title: Threat modeling, in the order the questions build on each other
scenario: threat model, threat modeling, what can go wrong, STRIDE, trust boundaries, data flow diagram, security design review, new feature security
roles: [threat-modeler, security-reviewer, solution-architect]
sources: [S-044, S-045, S-046]
---

# Threat modeling, in the order the questions build on each other

## Purpose
Find and handle security threats while the design can still change. This is a process because each step needs the one before: threats cannot be found in a system nobody described, responses cannot be chosen for threats nobody ranked, and nobody can say the work was good enough before the responses exist.

## Trigger
A new system or feature, or a change that moves a trust boundary, a data flow or the exposure of something. Ideally early in design; the model is kept up to date as the system changes.

## Participants
Whoever knows the design (developers, architects), a security voice, and the stakeholders who confirm the result.

## Inputs
- The design, architecture or feature description, and any known deployment exposure.

## Outcomes
- A system model, ranked threats, a response and owner for each, security requirements that can be tracked, and a confirmed review.

## How it is handled
- What are we working on: map the system, for example with a data flow diagram or by brainstorming; identify trust boundaries, data flows, data stores, processes and external entities, which are the likely attack points; write down assumptions.
- What can go wrong: find threats with a stated method (STRIDE checks six categories against each component and flow) and rank them by likelihood and impact, taking into account the effort to fix them.
- What are we going to do about it: choose mitigate, eliminate, transfer or accept for each threat; turn agreed mitigations into security requirements and track them.
- Did we do a good enough job: stakeholders confirm the model is accurate, complete and documented, and that the mitigations can be tested.
- Cloud-native and hybrid systems add shared responsibility, managed services, identity federation and dynamic infrastructure to the model.

## Expectations of the position
- **Threat modeler:** produces the model and keeps the method and the unknowns explicit; does not need to be a security expert, since the technique is meant for developers, designers and architects.
- **Architect and developers:** supply the design truthfully and own the mitigations in their area.
- **Security reviewer:** challenges the model independently of the design's own claims.

## Sources
S-045 (primary, read in full page) gives the four steps and the response options. S-046 (primary, read) gives the STRIDE categories. S-044 (primary) was read only through a search summary because the site did not load; the four-question framing there agrees with S-045. The Threat Modeling Manifesto's values and principles were not read.
