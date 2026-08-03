---
summary: Devops module, six rules and four wargames on hosting, artefacts, restores and spend
type: doctrine
tags: [ops]
status: archived
---

# Devops

The module that owns how ventures run: hosting, deploy artefacts,
environments, secrets, backups, spend. Populated at F3 from WiseWattage
(Railway deploys, the migration runner, determinism fixes), AutoWatt's
ADR-0002 (the AWS estate, local harness mandate, restore-test cadence,
contractual spend rule) and the PatterTech_Website static profile.

## Activation triggers

Any venture that deploys anywhere, stores data, or spends money on
infrastructure. The hosting and container forks are walked at Session
0 whenever a deploy exists; the restore fork activates with the first
production data; the cost fork with the first paid tier or the first
unattended fleet.

## What lives where

- The six binding rules: `DOCTRINE.md`.
- The four forks: `wargames/` (WG-OPS-001 hosting, 002 containers, 003
  backups and restore, 004 cost ceilings).
- Exact platforms, versions and caps: the stack profiles in
  `registry/stacks/` and the venture's ADRs, cited from rulings.
- The deploy and incident procedures: the kernel playbooks PB-031 and
  PB-032, compiled into L ventures, backed by venture runbooks.
