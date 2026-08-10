---
summary: Cold-agent acceptance drill for the native-client pack, an offline-capable client with a declared conflict policy and a forward-only release path
type: example
tags: [eos, testing]
---

# Drill: the write that survives the tunnel

Proposed here, then frozen. The spec of record is
`benchmark/drills/native-client.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/native-client.md`
- Run it: `python -m tools.eos drills --pack native-client`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
