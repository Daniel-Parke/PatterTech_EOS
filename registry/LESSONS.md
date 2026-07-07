---
summary: The harvest ledger, lessons from the estate and what each one changed
type: registry
tags: [eos]
status: active
review_by: 2026-10
---

# LESSONS

The harvest ledger. Every entry carries a disposition: ruling appended,
wargame filed, default changed, registry row amended, or declined with a
reason. A silent harvest month still records "checked, clean". Seeded
below from the estate survey at EOS creation.

| Date | Lesson | Source | Disposition |
| --- | --- | --- | --- |
| 2026-07 | urllib3 2.5+ breaks Railway startup; cap `<2.5.0` until a deploy proves otherwise | WiseWattage | Registry note here; goes into STACK-fastapi-postgres (Phase A follow-up) |
| 2026-07 | Docker builds on Windows fail on pnpm symlinks unless `**/node_modules` is dockerignored | WiseWattage | Same stack profile note |
| 2026-07 | Generated artefacts (OpenAPI types, schemas) must be committed with a CI drift check, or they rot silently | WiseWattage | Architecture module mandate (Phase F) |
| 2026-07 | Visual regression needs a Docker-pinned image or fonts diverge across machines | WiseWattage | Delivery module mandate (Phase F) |
| 2026-07 | Migrations: forward-only, idempotent, advisory-locked, run before app start, fail closed | WiseWattage | Devops module mandate (Phase F) |
| 2026-07 | Hydration warnings are often extension noise; verify in a clean profile before treating as a bug | WiseWattage | Lesson row only, declined as doctrine (too narrow) |
| 2026-07 | Ratcheting gates (mypy allowlist, coverage floors) beat big-bang strictness | WiseWattage | Delivery module mandate (Phase F) |
| 2026-07 | Plan/build decoupling: agent-driven planning, deterministic byte-stable build, nothing generative in the build step | PatterTech_Business | Became EOS principle 3 (compiled, never composed) |
| 2026-07 | Stale docs are a bug: delete, ban-list the old path in a test, never archive-in-place | WiseWattage | Absorbed into GOVERNANCE supersession rules |
| 2026-07 | A design law that lives one directory away from the code might as well not exist | PatterTech_Website v4 | WG-WEB-013 filed (by Daniel) |
| 2026-07 | Uniform ceremony kills small work; a bug fix must never need sixteen acceptance criteria | External (SDD research) | Became the scale system and WG-EOS-001 mandate |
