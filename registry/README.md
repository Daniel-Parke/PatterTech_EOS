---
summary: Entry point for dated EOS facts, evidence, lessons, coverage, aliases and stack profiles
type: registry
tags: [eos]
status: active
review: 2027-08
---

# Registries

Registries hold dated facts and machine-readable ledgers. They do not replace
standing Doctrine.

| Canonical record | What it owns | Reader view |
| --- | --- | --- |
| `coverage.json` | Built and registry-only capability status | `CAPABILITIES.md` |
| `evidence.json` | Sources and the claims drawn from them | none |
| `lessons.json` | Harvested lessons and their dispositions | `LESSONS.md` |
| `pressure-dispositions.json` and pack `relations/` | Pressure coverage and typed Doctrine Relations | `DOCTRINE_PRESSURE_MATRIX.md` |
| `identifier-aliases.json` | Direct compatibility aliases | `IDENTIFIER_ALIASES.md` |
| `PROJECTS.md` | Dated venture directory | same file |
| `stacks/` | Tested tool combinations and interoperability limits | same files |

Files marked `derived: true` are generated. Change their canonical source and
run `python -m tools.eos check --write-index`; never edit the view directly.

Stack profiles are dated facts. Named tools, tested versions and performance
observations belong there rather than in timeless Doctrine. Raw venture
Rulings remain venture-owned. Only privacy-reviewed, sanitised summaries may
enter the EOS lessons or examples.
