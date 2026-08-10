---
summary: Cold-agent acceptance drill for the marketing-growth pack, one launch surface plus one lifecycle sequence, machine-checked
type: example
tags: [eos, testing]
---

# Drill: a launch page and a first email, both provable

Proposed here, then frozen. The spec of record is
`benchmark/drills/marketing-growth.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/marketing-growth.md`
- Run it: `python -m tools.eos drills --pack marketing-growth`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
