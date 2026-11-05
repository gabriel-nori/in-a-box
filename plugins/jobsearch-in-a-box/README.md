# jobsearch-in-a-box

Role: **Job-search assistant**. Accountable for finding fitting vacancies, comparing each honestly against the candidate, drafting documents that claim only true facts, and tracking every application to its outcome. It drafts and never sends.

Skills: [`job-profile`](skills/job-profile/SKILL.md) produces `verified-profile`; [`job-scout`](skills/job-scout/SKILL.md) produces `shortlist`; [`posting-analyst`](skills/posting-analyst/SKILL.md) produces `requirement-match`; [`cv-tailor`](skills/cv-tailor/SKILL.md) produces `tailored-cv`; [`cover-letter-writer`](skills/cover-letter-writer/SKILL.md) produces `cover-letter`; [`application-mailer`](skills/application-mailer/SKILL.md) produces `mail-draft`; [`application-tracker`](skills/application-tracker/SKILL.md) produces `application-board`.

Script (Python 3, standard library, no network): `scripts/jobkit.py`
- `guard --draft F --source F...`: names, numbers and credentials in a draft that no source backs; exit 2 if any.
- `years ROLES.json`: years of experience with overlapping roles counted once.
- `band SCORE`: the fit band.
- `dedupe POSTINGS.json [--seen SEEN.json]`: drops postings seen before and the same job twice.

The profile is personal and lives in the owner's brain, never in this repo.

## Inspiration

The idea of one verified profile, a per-posting match with visible gaps, drafts built only from true facts, and a board from draft to offer comes from [AienTech/dossier](https://github.com/AienTech/dossier), which is AGPL-3.0. This plugin was written from its README and design, reading its approach; no code, prompt text or assets were copied, and the structure here is different (skills as contracts, a guard in code, the brain as the store).
