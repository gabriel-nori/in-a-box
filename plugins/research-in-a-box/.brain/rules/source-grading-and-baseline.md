THE RULE

A source is cited only to the depth it was read, and a refresh is a diff against a baseline fixed beforehand.

- Primary is the standard, law, official documentation or guide itself; secondary is a summary, training page or vendor blog about it. Say which, in the same line as the claim.
- Read status is `page` (fetched and read), `partial` (part came through) or `search` (only a result summary). A claim never reaches past its read status.
- A page that fails (403, 404, 429, empty, DNS) gets one alternative, then goes to `Tried and not read` with the effect on the claim.
- The baseline is the registry and its claims before the run. On a refresh, report added, removed and changed sources, read-status upgrades and downgrades, and per claim stronger, weaker, contradicted or unchanged.
- Where only secondary sources exist, say no authoritative source was found.

WHY

Trigger: someone asks to research a topic, enrich a skill, or redo earlier research.

A citation is only useful if a reader can tell how much weight it carries. Without a fixed baseline a refresh compares the result to itself and reports nothing. This rule is this repo's own practice (CONVENTIONS section 10), not an external standard.

HOW TO APPLY

Search by standard name and publisher, then fetch the page; record one registry row per source with the next free id. Fix the baseline before the first registry edit (`scripts/sources-diff.py --base <ref>`). Search queries carry the topic only, never personal or confidential context. Route each finding: brain rule, process (only where the source fixes an order), skill clause, or nowhere.

RELATED

Skill: source-researcher. Registry: docs/research-sources.md. No external source; this is a repo convention.
