THE RULE

A process model is valid when it is complete and renders: every path ends, every task has an actor, every gateway labels every outcome.

- Draw start and end events, tasks, and gateways as distinguishable shapes. In Mermaid `flowchart`: stadium for start and end, rectangle for a task, diamond for a decision, subgraphs for lanes.
- Mermaid is not BPMN. Message flows, boundary events and pools are not drawn natively; say so rather than imply them.
- Mermaid pitfalls: a lowercase `end` as a label breaks the diagram; a node name starting with `o` or `x` after `---` becomes a circle or cross edge; quote labels with special characters.
- As-is shows what runs today; to-be shows the target. Keep them separate and list the delta.

WHY

Trigger: someone asks to map, model or draw a process.

BPMN 2.0.2 is the OMG notation for business process diagrams. The page read did not describe gateways or events and the normative PDF was not read, so the completeness criteria above are the skill's contract, not a quotation of the standard.

HOW TO APPLY

Scope and actors first, then as-is, then to-be, then the delta. Check the Mermaid syntax against the pitfalls before delivering.

RELATED

Sources (S-063 partial, S-064 read). Skill: process-modeler.
