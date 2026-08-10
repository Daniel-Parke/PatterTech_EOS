---
summary: Single-run cold-agent acceptance drill for the support-operations pack, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# Drill: run one inbox week and one customer-visible incident

Proposed here, then frozen. The spec of record is
`benchmark/drills/support-operations.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/support-operations.md`
- Run it: `python -m tools.eos drills --pack support-operations`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
