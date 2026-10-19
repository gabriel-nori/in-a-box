# architect-in-a-box

Skills:

- [`solution-architect`](skills/solution-architect/SKILL.md): the base role. Designs the target architecture, compares platforms when undecided, records the decisions. Produces `architecture-design`.
- [`architect-aws`](skills/architect-aws/SKILL.md): specialises `solution-architect` for AWS, with a service map and the platform's design norms.
- [`architect-gcp`](skills/architect-gcp/SKILL.md): specialises `solution-architect` for GCP, with a service map and the platform's design norms.
- [`architect-azure`](skills/architect-azure/SKILL.md): specialises `solution-architect` for Azure, with a service map and the platform's design norms.
- [`architect-proxmox`](skills/architect-proxmox/SKILL.md): specialises `solution-architect` for Proxmox, with a service map and the platform's design norms.
- [`architect-vmware`](skills/architect-vmware/SKILL.md): specialises `solution-architect` for VMware, with a service map and the platform's design norms.

Rules for the brain live in [`.brain/rules`](.brain/rules): decide with records, design for failure and exit, verify provider facts. Import them under supervision with `python scripts/import-brain.py architect-in-a-box` (dry-run), then `--apply`.
