---
summary: The EOS heartbeat, what recurs, how often, and when each last ran
type: org
tags: [eos]
status: archived
---

# CADENCE

The EOS's recurring sessions. Cadences start once v1.0.0 ships; until
then every session is a build session against the queue. A due cadence
outranks new low-priority work. A cadence that finds nothing still
records checked, clean.

| Cadence | Playbook | Frequency | last_run | next_due |
| --- | --- | --- | --- | --- |
| Harvest | PB-E02 | Monthly | never | after v1.0.0 |
| Hygiene | PB-E09 | Monthly | never | after v1.0.0 |
| Promotion review | PB-E04 | Monthly | never | after v1.0.0 |
| Inception drill | PB-E07 | Quarterly | never | after v1.0.0 |
| Projects review | PB-E06 check | Quarterly | never | after v1.0.0 |
| Release | PB-E05 | On demand | never | v1.0.0 at queue end |
