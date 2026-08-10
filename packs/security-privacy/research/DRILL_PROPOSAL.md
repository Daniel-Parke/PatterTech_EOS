---
summary: Proposed cold-agent acceptance drill for the security, privacy and safety pack
type: example
tags: [eos]
---

# Drill proposal: the poisoned integration guide

Proposed here, then frozen. The spec of record is
`benchmark/drills/security-privacy.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/security-privacy.md`
- Run it: `python -m tools.eos drills --pack security-privacy`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
