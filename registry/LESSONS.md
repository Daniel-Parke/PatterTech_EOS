---
summary: The harvest ledger, live lessons and their dispositions, plus what has been pruned into the packs
type: registry
tags: [eos]
status: active
review_by: 2026-11
---

# LESSONS

The harvest ledger. Every entry carries a disposition that points at the
file which now owns the decision: an evidence id, a guide or wargame id,
an RFC, or a plain decline with a reason. A silent harvest month still
records "checked, clean".

**A lesson leaves this ledger once its content is stated as a rule
somewhere else.** Keeping it here as well would be a second home for the
same rule, and one of the two homes would go stale. Rows that record
what changed and why are provenance, and those stay.

Nothing has been harvested under PB-E02 yet. The rows below came from
the estate survey at EOS creation and from the AutoWatt reseed feedback.

## Live rows

| Date | Lesson | Source | Disposition |
| --- | --- | --- | --- |
| 2026-07 | Hydration warnings are often browser-extension noise; verify in a clean profile before treating one as a bug | WiseWattage | Declined. Too narrow to bind, and no pack owns it. No guide id and no evidence row, on purpose |
| 2026-07 | Plan and build decouple: agent-driven planning, a deterministic byte-stable build, nothing generative in the build step | PatterStudio | Became an EOS principle, "compiled, never composed", in `README.md`, and the compile contract in `kernel/README.md` |
| 2026-07 | Stale docs are a bug: delete them, ban-list the old path in a test, never archive in place | WiseWattage | Absorbed into the supersession rules in `GOVERNANCE.md` |
| 2026-07 | A design law that lives one directory away from the code might as well not exist | PatterTech_Website v4 | WG-WEB-013 filed by Daniel, now at `archive/v1/doctrine/web-design/wargames/WG-WEB-013-kit-escape-and-enforcement.md`, and carried into `packs/ui-ux/guides/GD-UIUX-004-token-source.md` |
| 2026-07 | Uniform ceremony kills small work; a bug fix must never need sixteen acceptance criteria | External research | Became the scale system and the WG-EOS-001 mandate, and then the whole of the v2 kernel: modes, tiers and ceremony budgets, ADR-0002 |
| 2026-07 | Template boilerplate that states venture history must be a slot; a reseed with real history should fill it, not overwrite it | AutoWatt reseed | Default changed: `kernel/templates/org/CONSTITUTION.tpl.md` gained the amendment-history slot |
| 2026-07 | The dark-first surface register loses to print-native institutional brands; the ink-like clause carried a real venture | AutoWatt reseed | Argued ruling appended to WG-WEB-001, now at `archive/v1/doctrine/web-design/wargames/WG-WEB-001-surface-register.md`. One argued ruling from one venture, so it is not yet promotion evidence; the philosophy question it raises is carried by `packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md` |
| 2026-07 | Reseeds meet pre-EOS files; the ancestry table needs normalised and preserved row kinds beyond compiled and authored | AutoWatt reseed | Default changed: `kernel/templates/COMPILE_REPORT.tpl.md` documents both kinds |

## Pruned

Seven rows left this ledger in the v2 build because their content is now
stated as a rule elsewhere. Recorded here so the harvest history stays
readable, one line each, no rule text.

| Lesson | Now owned by |
| --- | --- |
| Cap urllib3 below 2.5 until a deploy proves otherwise | `registry/stacks/STACK-fastapi-postgres.md` |
| Dockerignore node_modules or Windows pnpm symlinks break the build | `registry/stacks/STACK-fullstack-app.md` |
| Generated artefacts must be committed with a drift check or they rot | `packs/architecture/PACK.md` and its CHECKS row, argued in WG-ARCH-005 |
| Visual regression needs a pinned image or fonts diverge across machines | `packs/delivery-testing/PACK.md`, argued in WG-DEL-003 |
| Migrations: forward-only, idempotent, advisory-locked, run before app start, fail closed | `packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md` |
| Ratcheting gates beat big-bang strictness | `packs/delivery-testing/refs/QUALITY_SIGNALS.md` and its CHECKS rows |
| The prune-and-fill compile is mechanical enough to script | `inception/INCEPTION.md` phase D |
