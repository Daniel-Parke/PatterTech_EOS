---
summary: Pointer, the EOS heartbeat is machine state in org/cadence.json
type: org
tags: [eos]
---

# CADENCE

The cadence rows live in `org/cadence.json`: id, frequency, last_run,
next_due and a procedure pointer into `org/PLAYBOOKS.md`. Rows fire
under v2 rules once v2 releases; next_due dates count from the v1.0.0
tag date, 2026-07-07. The v1 table is archived at
`archive/v1/org/CADENCE.md`.
