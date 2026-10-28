THE RULE

A skill is integrated when everything that mirrors it agrees and everything that depends on it has been looked for.

- Placement follows the one-role rule: an existing role takes a router, specialist or stage; a new role is a new plugin.
- Edges, specializations, README row, manifest and maps mirror the skill. Manifest skill lists and maps are generated, never typed.
- A change is additive, breaking or patch. Renaming or removing a clause, skill or artifact, or tightening a `Requires`, is breaking and bumps the plugin version accordingly.
- Before calling a change safe, search the tree for the skill name, the artifact name and each clause name.
- The checker's output is the evidence; brain import is a dry-run until the owner approves.

WHY

Trigger: a skill is added to the tree or an existing one is changed.

Flows and team rules aim at clause and artifact names, so an unnoticed rename silently breaks them. This rule is this repo's own practice (CONVENTIONS sections 3, 7, 8, 9), not an external standard.

HOW TO APPLY

Scaffold a new role with `scripts/new-plugin.py`; run `scripts/sync-manifest.py` and `scripts/gen-maps.py`; run `scripts/check-contracts.py` and quote it. List every consumer of a breaking change with the edit made or who owns it. Restate any constraint from a deleted step as a guardrail first.

RELATED

Skill: skill-integrator. Depends on research via source-researcher when norms are being refreshed. No external source; this is a repo convention.
