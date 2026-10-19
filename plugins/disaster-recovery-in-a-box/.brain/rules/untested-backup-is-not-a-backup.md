THE RULE

A backup counts only after a restore from it has been verified, including that the data is usable by the application. Backups also live outside the failure domain they protect against: another account, region or site, with separate credentials, and immutable or offline where ransomware is in scope.

- Record the date of the last successful restore test per dataset.
- Replication is not backup: it copies deletion and corruption too.
- The restore path must not depend on the system that failed (identity, DNS, secrets, the runbook itself).

WHY

Backup jobs that report success regularly produce unusable data, and a backup reachable with the same credentials as production falls with it.

HOW TO APPLY

For each dataset list location, isolation, retention, immutability and last verified restore. Anything without a verified restore is marked unverified in the plan.

EXCEPTIONS

Data that is cheaply rebuilt from a verified source may be exempt if the rebuild itself is tested.

JUDGED AGAINST

Every protected dataset has a restore-test date or is marked unverified.

RELATED

disaster-recovery targets-from-impact; security least-privilege
