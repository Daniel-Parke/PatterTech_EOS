---
summary: The module map, what is populated, what is queued, and the extraction mandates
type: governance
tags: [eos]
status: archived
---

# Doctrine modules

The knowledge half of the EOS. Module shape and leanness rules are in
`MODULE_SHAPE.md`; every wargame in every module is indexed in
`WARGAME_INDEX.md`.

## Module map

| Module | Status | Covers |
| --- | --- | --- |
| `web-design/` | Populated | Web design, UI/UX, front-end implementation, QC gates |
| `voice/` | Queued (Phase C) | The house voice law, registers, banned patterns |
| `architecture/` | Queued (Phase F) | System boundaries, ADR practice, deterministic builds, contracts |
| `delivery/` | Queued (Phase F) | Testing strategy, CI, gate rubrics, release discipline |
| `devops/` | Queued (Phase F) | Hosting, environments, migrations discipline, cost triggers |

## Roadmap rows (v1.1 and beyond)

Extraction mandates for modules that wait until a venture or the harvest
demands them:

- **data**: schema standards, retention and redaction patterns, integrity
  checks. Extract from WiseWattage (`database/`, TimescaleDB practice)
  and the AutoWatt field-continuity doctrine.
- **security-compliance**: threat models, the REG registry pattern in
  full, privacy artefacts. Extract from the AutoWatt compliance registry
  (REG-COMP-UK-001) and WiseWattage auth and rate-limit practice. The
  registry pattern itself ships in the kernel already.
- **product**: brief-to-spec methods, vocabulary discipline, acceptance
  walk-throughs. Extract from the AutoWatt product brief and Genesis.
- **hardware**: selection and sizing. Waits for a venture that needs it
  (PatterOS is the likely source).

Cost is deliberately not a module: it is a trigger inside architecture
and devops wargames, and a column in stack profiles.
