---
id: online-index-change
title: Online index and schema change
scenario: create index on a big table, add an index without locking, alter table on production, concurrently, migration locks
roles: [dba, dba-postgres, developer-sql]
sources: [S-032, S-031]
---

# Online index and schema change

## Purpose
Change an index or schema on a live table without blocking writes longer than the business accepts, and with a way back.

## Trigger
A migration adds or changes an index or column on a table that is in use.

## Participants
The developer, the DBA and whoever approves production changes.

## Inputs
- The statement, the engine and version, the table's size and write rate, the lock behaviour of the operation.

## Outcomes
- A rollout plan that states lock behaviour, the online option, validation, and rollback.

## How it is handled
- In PostgreSQL, a plain `CREATE INDEX` blocks writes for the scan; `CREATE INDEX CONCURRENTLY` does not, at the price of two scans, waiting on older transactions, and no use inside a transaction block.
- A failed concurrent build leaves an INVALID index that queries ignore but writes still pay for: drop it and retry, or `REINDEX INDEX CONCURRENTLY`.
- Partitioned tables do not support concurrent builds directly; check the version's documentation.
- State a restore point before the change, and validate the index after.

## Expectations of the position
- **DBA:** names lock behaviour and rollback before the change runs.
- **Developer:** does not ship a blocking migration to a large live table.

## Sources
S-032 (PostgreSQL docs, primary, read). Behaviour for MySQL and SQL Server is carried by the specialist skills' own text, not sourced here.
