# infra-in-a-box

Role: **Infra Engineer**. Accountable for making sure software has an environment it can run, deploy and be observed in, reproducibly.

Skill: [`infra-engineer`](skills/infra-engineer/SKILL.md). Produces `environment-notes`.

## Specialists

`infra-engineer` is the base contract. `infra-terraform`, `infra-pulumi`, `infra-cloudformation`, `infra-puppet` and `infra-ansible` specialise it for one toolchain each: same contract plus a reviewed preview (plan, preview, change set, noop, check mode), state or stack safety, and secret handling for that tool. A flow that names `infra-engineer` is satisfied by any of them; pick the one that matches the repo's existing IaC.
- [`infra-ansible`](skills/infra-ansible/SKILL.md): specialises `infra-engineer` for Ansible (check mode first, idempotence, vault, scoped rollout).
