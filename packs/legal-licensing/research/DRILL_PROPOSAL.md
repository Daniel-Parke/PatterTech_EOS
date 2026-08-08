---
summary: Proposed cold-agent acceptance drill for the legal, licensing and compliance routing pack
type: example
tags: [eos, testing]
---

# Drill proposal: the waitlist feature with a poisoned dependency tree

Proposed here, then frozen. The spec of record is
`benchmark/drills/legal-licensing.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/legal-licensing.md`
- Run it: `python -m tools.eos drills --pack legal-licensing`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
