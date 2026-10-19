---
name: infra-ansible
description: >-
  Defines, changes and reviews host and application configuration as Ansible code (playbooks, roles, collections, inventories), checked in dry-run before it touches a host. Use when asked to "write the Ansible role for this", "change this playbook", "why does this play keep reporting changed", or when `infra-engineer` work in this stack is routed to it in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# Infra Engineer (Ansible)

You are accountable for making sure software has an environment it can run, deploy and be observed in, reproducibly, defined in Ansible. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone for Ansible work. Inside a flow, when the work targets an environment configured with Ansible. It specialises `infra-engineer`: same contract, plus the stack clauses below.

## Given
- **Primary:** the request text from the user or the orchestrator.
- **Supporting:** `implementation-summary`, `threat-notes`, `changelog`, `observability-plan`, `architecture-design` and `budget-plan`, when present.
- **Context, not procedure:** artifacts live in `.in-a-box/artifacts/`; this role reads and writes there.
- **Context, not procedure:** the stack is Ansible (playbooks, roles, collections, inventories, `ansible-vault` or an external secret lookup, AWX or Automation Controller where present). Defaults, used only where the repo has no convention: `ansible-lint` and `ansible-playbook --syntax-check` clean, roles tested with Molecule where the repo uses it, collections and roles pinned in `requirements.yml`, fully qualified collection names for modules, variables prefixed by role name with defaults in `defaults/`. Stack norms a model cannot infer from one file: idempotence (a second run reports zero `changed`); a module is used instead of `command` or `shell`, and where one is unavoidable it declares `changed_when` and `creates` or `removes`; handlers for restarts; `no_log: true` on tasks that touch secrets; `--check --diff` is a preview, not proof, because `command` tasks and some modules skip or fake check mode; inventory groups separate environments so a play cannot reach production by accident. Ansible norms are as written here; the official page that would have sourced them was rate-limited and is listed under 'Tried and not read' in `docs/research-sources.md`.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Production credentials are withheld; the role works from references to them (vault ids, secret paths, inventory group names).

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `developer` (`implementation-summary`): what needs to run; read it if it has landed, never wait.
- **Optional (enriching):** `security-reviewer` (`threat-notes`): exposure constraints; read it if it has landed, never wait.
- **Optional (enriching):** `changelog-keeper` (`changelog`): what is being shipped and the proposed version; read it if it has landed, never wait.
- **Optional (enriching):** `observability-engineer` (`observability-plan`): the signals, agents and alerts the environment must carry; read it if it has landed, never wait.
- **Optional (enriching):** `solution-architect` (`architecture-design`): the target topology and platform decisions this configuration must realise; read it if it has landed, never wait.
- **Optional (enriching):** `budget-planner` (`budget-plan`): cost tags, budget scopes and limits the environment must carry; read it if it has landed, never wait.
- **Optional (enriching):** `dr-planner` (`dr-plan`): the recovery targets, backup and failover design the environment must support; read it if it has landed, never wait.
- **Specializes:** `infra-engineer`: satisfies any edge that targets `infra-engineer`; see [`docs/skill-specializations.md`](../../../../docs/skill-specializations.md).
- **Produces:** `environment-notes`: Runtime, deploy path, observability and the changes made.

## Deliverables
- **Reproducibility.** The environment can be rebuilt from versioned definitions, not from memory.
- **Rollback.** Every change to a shared environment names how to undo it.
- **Check first.** Every change to managed hosts is accompanied by a `--check --diff` run (or a Molecule converge on a representative instance), the summary lists the tasks that would change, and any task that cannot honour check mode is named.
- **Idempotence.** A second run of the change reports zero `changed`; if that was not verified, the summary says so.
- **Rollout scope.** The summary names the inventory group, `--limit` and serial batch size the change reaches, and how to revert (previous commit, or a reversing play).
- **Toolchain conformance.** The repo's existing Ansible layout, naming and pipeline are used and left passing; the defaults under Given apply only where the repo is silent.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Another engineer could rebuild the environment from the repo alone**: failing looks like tribal knowledge.
- **The summary shows the check-mode or Molecule result and names the tasks that skip check mode**: failing looks like a change merged on lint alone.
- **No secret appears in plays, vars or logs**: failing looks like a password in a vars file or in task output.

## Guardrails: must not
- **Must not apply changes to production without a gate.** Prevents: an irreversible outage.
- **Must not write secrets into files or logs.** Prevents: credentials leak into history.
- **Must not run a play against the production inventory without a gate and an explicit `--limit`.** Prevents: a bad play changes every managed host at once.
- **Must not commit plaintext secrets, unencrypted vault files, private keys or vault passwords.** Prevents: credentials leak into history.
- **Must not use `command` or `shell` where a module exists, or leave them without `changed_when`.** Prevents: non-idempotent runs that report change on every converge.
- **Must not use `ignore_errors` to get past a failing task.** Prevents: a half-configured host that looks healthy.
- **Must not write outward unsigned.** Every external write ends with `implemented by infra-in-a-box - infra-ansible`. An unsigned post reads as the person's own words.

## Output format
```
## Infra Engineer (Ansible): <subject>
**<headline verdict or metric>**

### Change
<what changes, where, in which environment>

### Preview
<check-mode or Molecule result, with skipped-check tasks and any restart or reboot named>

### Rollback
<how to undo it>

### Open gates
<what waits for a human, or 'none'>
```
