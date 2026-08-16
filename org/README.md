---
summary: Entry point for operating and changing the EOS itself
type: org
tags: [eos]
---

# Operating the EOS

This directory holds the EOS's own work state and change process. Start with
`STATE.md` for current claims and flags, then `TASKS.md` for the task table.
Both are generated from records under `tasks/` and `claims.json`; edit the
source and run `python -m tools.eos task views`.

Use `PLAYBOOKS.md` for repeatable EOS procedures and `decisions/` for accepted
architecture and governance decisions. `logs/` and `reports/` are dated
records, not current operating instructions. Migration inventories and
ledgers live under `migration/`.

For substantial parallel work, follow the Agent Build Orchestration pack.
The integrator commits claims before dispatch, owns shared files and generated
views, and verifies the merged result. A lone writer is implicitly claimed.

Changes to the protected set require an accepted ADR and the operator, as
defined in `GOVERNANCE.md`. Finish repository work with
`python -m tools.eos check --repo` and the full test suite.
