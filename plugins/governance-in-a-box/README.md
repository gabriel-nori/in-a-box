# governance-in-a-box

Skills:

- [`policy-author`](skills/policy-author/SKILL.md): writes and maintains policies, standards and exceptions, each with owner, source, review date and an expiring exception route. Produces `policy-set`.
- [`risk-register`](skills/risk-register/SKILL.md): identifies and scores risks (ISO 31000), sets treatment and owners, and tracks appetite and acceptances. Produces `risk-register`.
- [`controls-auditor`](skills/controls-auditor/SKILL.md): read-only; maps controls to ISO/IEC 27001, 27701 and 42001, SOC 2, LGPD, GDPR, CIS and others, including data and AI governance, and reports evidence and gaps. Produces `control-findings`.
- [`decision-steward`](skills/decision-steward/SKILL.md): keeps the RACI, approval matrix, decision records (ADRs) and change process. Produces `decision-log`.

Out of scope here because it has a home: technical security review (`security-in-a-box`), legal reading of LGPD and contracts (`lawyer-in-a-box`), continuity and disaster recovery (`disaster-recovery-in-a-box`), cloud guardrails and landing zones (`architect-in-a-box`), cost governance (`finops-in-a-box`). Governance consumes their artifacts.

Rules for the brain live in [`.brain/rules`](.brain/rules): every rule has an owner and an expiry route, risk acceptance needs a named person, control status needs evidence of operation, decisions keep their reasons and are superseded rather than rewritten. Import them under supervision with `python scripts/import-brain.py governance-in-a-box` (dry-run), then `--apply`.