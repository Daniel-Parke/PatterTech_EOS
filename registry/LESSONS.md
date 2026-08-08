---
summary: The harvest ledger, live lessons and their dispositions, plus what has been pruned into the packs
type: registry
tags: [eos]
status: active
review: 2026-11
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

The first PB-E02 harvest ran on 2026-08-08 against the three governed
ventures. Venture A's two entries had both already been folded during the
v1 build and are recorded as such below. Guth's feedback file carried
fifteen entries and a matured stack profile, and is the substance of
this harvest. PatterTech_Website ships no feedback file: it predates the
template, which is itself a finding and is queued.

Earlier rows came from the estate survey at EOS creation and from the
Venture A reseed feedback.

The PB-E04 promotion review ran the same day and promoted nothing. The
sample: zero live `lifecycle: experimental` items, so nothing expired
past the ninety-day window; zero `lifecycle: contested` rules; the
twenty-four binding rules in `packs/` unchanged; and no exception ledger
to sample, because `org/exceptions.jsonl` was specified and never
implemented, which is itself queued. Of the harvest's three promotion
candidates, each carries one argued ruling from one venture, which under
the ladder in `GOVERNANCE.md` is short of binding-candidate. Guth's five
draft wargames stay candidates for the same reason: a fork that happened
once is not a recurring fork, and a guide written for it would be
speculation with a filename.

## Live rows

| Date | Lesson | Source | Disposition |
| --- | --- | --- | --- |
| 2026-07 | Hydration warnings are often browser-extension noise; verify in a clean profile before treating one as a bug | WiseWattage | Declined. Too narrow to bind, and no pack owns it. No guide id and no evidence row, on purpose |
| 2026-07 | Plan and build decouple: agent-driven planning, a deterministic byte-stable build, nothing generative in the build step | PatterStudio | Became an EOS principle, "compiled, never composed", in `README.md`, and the compile contract in `kernel/README.md` |
| 2026-07 | Stale docs are a bug: delete them, ban-list the old path in a test, never archive in place | WiseWattage | Absorbed into the supersession rules in `GOVERNANCE.md` |
| 2026-07 | A design law that lives one directory away from the code might as well not exist | PatterTech_Website v4 | WG-WEB-013 filed by Daniel, now at `archive/v1-final:doctrine/web-design/wargames/WG-WEB-013-kit-escape-and-enforcement.md`, and carried into `packs/ui-ux/guides/GD-UIUX-004-token-source.md` |
| 2026-07 | Uniform ceremony kills small work; a bug fix must never need sixteen acceptance criteria | External research | Became the scale system and the WG-EOS-001 mandate, and then the whole of the v2 kernel: modes, tiers and ceremony budgets, ADR-0002 |
| 2026-07 | Template boilerplate that states venture history must be a slot; a reseed with real history should fill it, not overwrite it | Venture A reseed | Default changed: `kernel/templates/org/CONSTITUTION.tpl.md` gained the amendment-history slot |
| 2026-07 | The dark-first surface register loses to print-native institutional brands; the ink-like clause carried a real venture | Venture A reseed | Argued ruling appended to WG-WEB-001, now at `archive/v1-final:doctrine/web-design/wargames/WG-WEB-001-surface-register.md`. One argued ruling from one venture, so it is not yet promotion evidence; the philosophy question it raises is carried by `packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md` |
| 2026-07 | Reseeds meet pre-EOS files; the ancestry table needs normalised and preserved row kinds beyond compiled and authored | Venture A reseed | Default changed: `kernel/templates/COMPILE_REPORT.tpl.md` documents both kinds |
| 2026-08 | A slot pattern that excludes digits lets a digit-bearing slot ship unfilled through a green seed check | Guth cold-start probe | Bug fixed: E008's `SLOT_RE` in `tools/eos/checks/structural.py` widened to `[A-Z0-9_]+`, with a regression test. `{{SUCCESS_90}}` in `kernel/templates/VENTURE_BRIEF.tpl.md` was the live instance |
| 2026-08 | A checker that walks every markdown file under the seed path fails on vendored dependency trees | Guth S1 | Already fixed in v2: `SKIP_DIRS` in `tools/eos/repo.py` skips `node_modules`, `.git`, `__pycache__` and `.pytest_cache`. Recorded as confirmation that the v2 rewrite closed it |
| 2026-08 | A claim protocol where the queue row and the claim are two edits lets two launchers collide on one item | Guth S1 | Fixed by design in v2: claims are coordinator-assigned and committed before dispatch, and lanes never acquire or mutate one (`kernel/schemas/claims.schema.json`) |
| 2026-08 | Inception necessarily writes to main, because the org that mandates branches is being compiled during the writes | Guth S1 | Queued as T-0005: `inception/INCEPTION.md` needs the one-line exemption so the first review session does not read Session 0 as a violation |
| 2026-08 | A cold-start probe run before the human rubric is signed surfaces real defects a warm session cannot see | Guth S1 | Promotion candidate for PB-E04. One argued ruling from one venture, so not yet binding evidence. The v2 drill apparatus is the natural home once it has graders |
| 2026-08 | A venture whose master prompt fixes deep product doctrine walks long at Session 0, because doctrine engages triggers the interview leaves silent | Guth S1, 32 rulings against a 20 budget | Queued as T-0006: `inception/WALK_ORDER.md` should count interview-triggered and doctrine-triggered rulings separately rather than budgeting them as one number |
| 2026-08 | A local-first browser product with a WASM compute core is a distinct proven shape, not a bend of the fullstack profile | Guth S1 | Registry addition: `registry/stacks/STACK-local-first-pwa.md`, carrying S1's worked evidence and five sharp edges |
| 2026-08 | Platform-native deployment beats the container default on a sovereign LAN with no parity or handover trigger | Guth, WG-OPS-002 ruled contrary | Contrary evidence recorded against the container default. Under `GOVERNANCE.md` precedence this triggers review, never automatic demotion, and one ruling from one venture is not promotion evidence. Carried to `packs/devops-reliability` at the next authoring pass |
| 2026-08 | A split voice register, warm-guide for in-app coaching and peer-expert for docs, reads cleanly in practice | Guth, WG-VOX-001 ruled split | Early supporting evidence for the three-way voice scope in `packs/writing-content/guides/GD-WRIT-003-voice-scope.md`, which already sanctions per-surface splits |

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
