---
summary: Cold-agent acceptance drill for the AI, ML and LLM pack, build the gate before tuning the classifier
type: example
tags: [eos, testing]
---

# Drill proposal: AI, ML and LLM pack

Proposed here, then frozen. The spec of record is
`benchmark/drills/ai-ml-llm.md`, hashed in
`benchmark/drills/MANIFEST.json` and verified against that hash on
every drill run.

The full text used to sit here as well, byte for byte, with nothing
checking the two still agreed. A second copy of a frozen spec is a way
for the drill that runs and the drill the pack describes to drift
apart unnoticed, so this organ points at the one that runs.

- Read the spec: `benchmark/drills/ai-ml-llm.md`
- Run it: `python -m tools.eos drills --pack ai-ml-llm`
- Provenance, wave and freeze date: `benchmark/drills/MANIFEST.json`
