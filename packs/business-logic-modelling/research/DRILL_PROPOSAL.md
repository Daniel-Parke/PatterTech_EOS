---
summary: Single-run cold-agent acceptance drill for the business logic and modelling pack, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# DRILL-BLM-001: the invariant holds, in money and in time

Proposed here, then frozen. The spec of record is
`benchmark/drills/business-logic-modelling.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/business-logic-modelling.md`
- Run it: `python -m tools.eos drills --pack business-logic-modelling`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
