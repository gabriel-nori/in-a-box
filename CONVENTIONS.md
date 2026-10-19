# Conventions

Binding for every plugin in this repo. `scripts/check-contracts.py` enforces what can be enforced.

## 1. Language

Repo, docs, skills, commits and PRs are in English.

## 2. Skills are contracts

A skill declares what must be true when it finishes and which constraints it may not break. It never declares the keystrokes to get there.

Required sections, in this order:

1. `When to use`: the trigger, in the person's words.
2. `Given`: inputs, each with what it is for. Context the model cannot infer is named as context.
3. `Withheld`: what must never be passed in, and why. If nothing, one line saying so. Never omitted.
4. `Depends on`: prior steps and blockers as edges (section 3).
5. `Deliverables`: named clauses, each stating what must be true or exist.
6. `Judged against`: conditions checkable from the output alone.
7. `Guardrails: must not`: each with the failure it prevents.
8. `Output format`: the shape of what it hands back.

Defects: a numbered step list, "first... then...", a hand-maintained stage table inside a skill.

Four-case test for any sentence: keep a real dependency (in `Depends on`), keep an irreversible or outward action (as a guardrail or gate), keep knowledge the model cannot infer (in `Given`), and replace "telling it how" with a deliverable clause plus the guardrail the procedure was silently carrying.

When refactoring a procedural skill, restate every constraint that lived in a deleted step as a guardrail before deleting the step.

## 3. Dependency edges

Each skill's `Depends on` uses exactly these edge kinds:

- **Requires:** hard. Must have completed or the skill stops. A root role writes `Requires: none`.
- **Optional (ordered):** a blocker. May not run at all, but if active it runs first, because starting early makes the output wrong.
- **Optional (enriching):** read it if present, never wait. Starting early only makes the output thinner.
- **Produces:** the artifact, by name.

`docs/skill-dependencies.md` mirrors every edge. The two must agree.

## 4. Artifacts

Roles communicate only through named artifacts under `.in-a-box/artifacts/<name>.md` in the target workspace. A role never calls another role directly. That is what keeps roles reusable in any flow.

## 5. Flows belong to the orchestrator

No role plugin knows about any flow. Ordering, branching and gates live in flow definitions interpreted by `orchestrator-in-a-box`.

## 6. Outward actions

Anything irreversible or outward (send, publish, deploy, push, sign) is a gate: the flow pauses for a human unless the user has durably authorised that exact action. Every outward write is signed `implemented by <plugin_name - skill_name>`.

## 7. Plugins

- Named `<role>-in-a-box`; the orchestrator is the single exception by function, still `orchestrator-in-a-box`.
- One role per plugin. A second role means a second plugin. A role may ship several skills: a router, specialists, and the stages that belong to it.
- A specialist skill declares `Specializes: <base>` in `Depends on` and is mirrored in `docs/skill-specializations.md`. It keeps the base contract and satisfies any edge that targets the base.
- Every plugin ships `.brain/` (section 8).
- Plugin versions follow semver; a skill clause rename is breaking, because flows and team rules aim at clause names.

## 8. The `.brain` folder

Every plugin ships `.brain/` at its root so the brain can import it as learned skills and rules, with more room to customise in a supervised flow.

- `.brain/manifest.json`: `{"plugin", "skills": [{"name", "file"}], "rules": [{"id", "title", "file", "scenario", "non_negotiable"}]}`. Every `SKILL.md` is listed; `scripts/sync-manifest.py` keeps the skill list current and keeps the rules.
- `.brain/rules/<id>.md`: one rule per file, with the sections `THE RULE`, `WHY`, `HOW TO APPLY` (optional: `EXCEPTIONS`, `JUDGED AGAINST`, `RELATED`), each heading alone on its line.
- Rules are for behaviour worth recalling beyond one skill run (how to apply or read something, a standard). A skill's own guardrails stay in the skill.
- Import is supervised: `scripts/import-brain.py <plugin>` is a dry-run that lists items; `--apply` (optionally `--only <id>...`) writes them after the owner approves. Skills enter as learned skills with their dependency edges; rules enter with `source=learned`. Items already in the brain are skipped.
- Nothing personal goes in a manifest.

`scripts/check-contracts.py` fails on a missing manifest, an unlisted skill, a missing file or a rule without its three sections.

## 9. Maps

Maps are generated, never written. scripts/gen-maps.py reads every SKILL.md and writes plugins/<plugin>/.brain/MAP.md (skills, specializations, edges by kind, products, purpose, cross-plugin needs) and the root MAP.md (import instructions, plugin table, execution layers from Requires and Optional (ordered) edges, cross-plugin edges). The output is deterministic: no timestamps, sorted. The brain reads the root map, then the plugin maps it needs.

- After changing a skill, a plugin or an edge, run scripts/gen-maps.py and commit the maps with the change.
- scripts/check-contracts.py runs gen-maps.py --check and fails on a stale map or an ordering cycle.
- Anything that follows a fixed model (maps, manifests, scaffolds, tables mirrored from skills) is produced by code, not by hand or by a model.

## 10. Processes

The plugins are built to be used with the brain, so what they carry is processes, not commands. A process says what a position does in a situation, how it is handled and what is expected of whoever holds the position. The brain recalls it by its scenario; nobody types a command.

**A process exists only where the source fixes an order.** The test: does the source say that one step must complete before the next can start, and would doing them out of order produce a wrong result? If yes, it is a process (a command handoff briefs fully, transfers command explicitly and waits for acknowledgement; the four threat-modeling questions build on each other; a restore point is stated before a schema change and the result validated after). If no, it is not a process. Everywhere else:

- The **result** is stated in the skill's Deliverables and Judged against, and the **dependency edges** (section 3) decide what runs first. Nothing else orders the work.
- A **standard worth recalling** (a checklist, a set of principles, a set of definitions, what a position is expected to do) is a brain rule under `.brain/rules/` (section 8), cited to its sources in the rule's RELATED section.

Process format:

- A process is `plugins/<plugin>/processes/<id>.md`, the id equal to the file name. Front matter: `id`, `title`, `scenario` (the words that should bring it to mind), `roles` (skills that take part, all must exist) and `sources` (ids from `docs/research-sources.md`, at least one).
- Sections, in this order: `Purpose`, `Trigger`, `Participants`, `Inputs`, `Outcomes`, `How it is handled`, `Expectations of the position`, `Sources`. `Purpose` says why the order matters. A process may describe steps; a skill may not (section 2). The skill is the contract for one role, the process is how roles meet around an ordered situation.
- Every claim traces to a source. `Sources` says how each source was read (full page, partial, search summary) and what stays unconfirmed. A secondary source is labelled as such, and a thin process says it is thin.
- Sources live only in `docs/research-sources.md`: id, publisher, kind (primary or secondary), how it was read, URL. A source that could not be read goes to its `Tried and not read` table, never into a process as if read.
- `scripts/sync-manifest.py` lists processes in `.brain/manifest.json` from the files; `scripts/import-brain.py` imports them as `process` nodes linked to the role skills, under the same supervised dry-run as skills and rules; `scripts/gen-maps.py` lists them in the plugin maps; `scripts/check-contracts.py` fails on a missing section, an unknown role or an unknown source id.
- A command is a generated form of a process, for hosts and people without the brain: `process-to-command` in `orchestrator-in-a-box` produces it. The process stays the source of truth; a command is regenerated, never edited.

## 11. Reviewing and routing by stack

A skill that covers many stacks is a router with one specialist per stack (section 7). The router owns the verdict and the merged report; each specialist keeps the base contract and adds the clauses of its stack.

- A specialist can call auxiliary specialists, declared as `Optional (ordered)` edges when the auxiliary result must exist first (a SQL review before the language review that embeds the query) and as `Optional (enriching)` when it only adds evidence. The call is an edge, never a step.
- Norms a specialist applies carry the id of the source they come from (`docs/research-sources.md`). The repo's own conventions outrank any sourced norm, and a source that calls a recommendation optional is not turned into a blocker.
- Example: `code-reviewer` hands each changed file to `code-reviewer-python`, `-java`, `-android`, `-react`, `-sql` or `-iac`; each of those asks `code-reviewer-sql` about any query it finds, and `code-reviewer-sql` waits for `dba`.