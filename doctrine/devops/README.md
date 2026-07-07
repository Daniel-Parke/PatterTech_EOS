---
summary: Devops module, queued for Phase F, hosting, environments, migrations, cost triggers
type: doctrine
tags: [ops]
---

# Module: devops (queued)

Lands in Phase F (see `org/QUEUE.md`). Will cover forward-only
idempotent migrations, environment discipline, main-always-releasable,
secrets handling, backup and restore-test regimes, and the wargames for
hosting (Railway versus AWS versus Vercel), containers versus
buildpacks, and cost ceilings as decision triggers.

Extraction sources: WiseWattage (Railway Docker deploys, migration
ledger, CI gates), Venture A ADR-0002 (AWS App Runner shape), the
PatterTech_Website Vercel static profile. Shape per
`doctrine/MODULE_SHAPE.md`.

## Activation triggers

Any venture that deploys anywhere, stores data, or spends money on
infrastructure.
