---
summary: Derived view of the lessons ledger, every row with its disposition and reasoning
type: registry
tags: [eos]
status: active
review: on-change-of:registry/lessons.json
derived: true
---

# LESSONS

Derived from `registry/lessons.json` by
`python -m tools.eos check --write-index`. Do not hand-edit.

**Live: 15. Rejected: 1. Deferred: 0. Pruned: 9.** A rejected row
stays here with its reason, so the same proposal cannot arrive
twice unrecorded. A pruned row is provenance: its rule text now
lives in the file named beside it.

The lessons ledger. Two intakes write here: the harvest, which pulls
rulings and feedback from a governed venture, and the Study workflow,
which reads a named source through a lens contract. Every row carries
a disposition that points at the file which now owns the decision, and
a declined lesson keeps its reason, so a decline cannot be re-proposed
as if it had never been argued. A silent harvest month still records
"checked, clean".

Disposition is an enum. `kernel/schemas/lesson.schema.json` lists
the permitted values and refuses one that is not on the list, and
`TOUR.md` is the home for what they mean: its table under "The
eleven dispositions" defines all eleven. Each value names the kind
of home a decision found; the row's own `outcome` and `informs`
name the file that holds it now. The value `binding` is absent on
purpose: this ledger can propose a binding candidate and nothing
more, because binding needs an accepted ADR and Daniel under the
ladder in `GOVERNANCE.md`.

**A lesson leaves this ledger once its content is stated as a rule
somewhere else.** Keeping it here as well would be a second home for
the same rule, and one of the two homes would go stale. Rows that
record what changed and why are provenance, and those stay.

The first PB-E02 harvest ran on 2026-08-08 against the three governed
ventures. Venture A's two entries had both already been folded during
the v1 build and are recorded as such below. Guth's feedback file
carried fifteen entries and a matured stack profile, and is the
substance of this harvest. PatterTech_Website ships no feedback file:
it predates the template, which is itself a finding and is queued.

Earlier rows came from the estate survey at EOS creation and from the
Venture A reseed feedback.

The PB-E04 promotion review ran the same day and promoted nothing. The
sample: zero live `lifecycle: experimental` items, so nothing expired
past the ninety-day window; zero `lifecycle: contested` rules; the
twenty-four binding rules in `packs/` unchanged; and no exception
ledger to sample, because ADR-0004 withdrew `org/exceptions.jsonl` and
moved a one-off exception onto the task record it applies to. Of the
harvest's three promotion candidates, each carries one argued ruling
from one venture, which under the ladder in `GOVERNANCE.md` is short
of binding-candidate. Guth's five draft wargames stay candidates for
the same reason: a fork that happened once is not a recurring fork,
and a guide written for it would be speculation with a filename.

## Live

### LES-0002 · Plan and build decouple, and nothing in the build is generative

- **Lesson**: Plan and build decouple: agent-driven planning, a deterministic byte-stable build, nothing generative in the build step.
- **Origin**: harvest
- **Venture**: PatterStudio
- **Source note**: Recorded at EOS creation against PatterTech_Business and corrected to PatterStudio in the v2 pass on 2026-08-03.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Became an EOS principle, "compiled, never composed", in `README.md`, and the compile contract in `kernel/README.md`.
- **Scope**: eos-internal
- **Applies when**: Any pipeline where an agent plans and a tool builds. What pays is a build a second run reproduces byte for byte.
- **Informs**: README.md, kernel/README.md
- **Decided**: 2026-07

### LES-0003 · Stale docs are a bug, so delete them and ban-list the path

- **Lesson**: Stale docs are a bug: delete them, ban-list the old path in a test, never archive in place.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Absorbed into the supersession rules in `GOVERNANCE.md`.
- **Scope**: estate
- **Applies when**: Repositories where documentation ships with the code and a superseded document keeps its old path.
- **Informs**: GOVERNANCE.md
- **Decided**: 2026-07

### LES-0004 · A design law one directory from the code may as well not exist

- **Lesson**: A design law that lives one directory away from the code might as well not exist.
- **Origin**: harvest
- **Venture**: PatterTech_Website
- **Source note**: The v4 pass.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: WG-WEB-013 filed by Daniel, now at `archive/v1-final:doctrine/web-design/wargames/WG-WEB-013-kit-escape-and-enforcement.md`, and carried into `packs/ui-ux/guides/GD-UIUX-004-token-source.md`.
- **Scope**: estate
- **Applies when**: Products with a design system whose tokens are enforced somewhere other than the code that consumes them.
- **Informs**: WG-WEB-013, packs/ui-ux/guides/GD-UIUX-004-token-source.md
- **Decided**: 2026-07

### LES-0005 · Uniform ceremony kills small work

- **Lesson**: Uniform ceremony kills small work; a bug fix must never need sixteen acceptance criteria.
- **Origin**: harvest
- **Venture**: External research
- **Source note**: Recorded at EOS creation as "External (SDD research)", in the estate survey rather than from a venture. No evidence row was written for it at the time and none has been written since.
- **Evidence class**: asserted
- **Disposition**: estate-default
- **Outcome**: Became the scale system and the WG-EOS-001 mandate, and then the whole of the v2 kernel: modes, tiers and ceremony budgets, ADR-0002.
- **Scope**: eos-internal
- **Applies when**: Any process applying one ceremony to work of different sizes. It stands on the practice that followed rather than on a cited source.
- **Informs**: WG-EOS-001, ADR-0002, kernel/SCALE_MATRIX.md
- **Decided**: 2026-07

### LES-0006 · Venture history in a template must be a slot, not boilerplate

- **Lesson**: Template boilerplate that states venture history must be a slot; a reseed with real history should fill it, not overwrite it.
- **Origin**: harvest
- **Venture**: Venture A
- **Source note**: Reseed feedback.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Default changed: `kernel/templates/org/CONSTITUTION.tpl.md` gained the amendment-history slot.
- **Scope**: eos-internal
- **Applies when**: Compiling a template into a repository that already has history worth preserving.
- **Informs**: kernel/templates/org/CONSTITUTION.tpl.md
- **Decided**: 2026-07

### LES-0007 · Dark-first loses to print-native institutional brands

- **Lesson**: The dark-first surface register loses to print-native institutional brands; the ink-like clause carried a real venture.
- **Origin**: harvest
- **Venture**: Venture A
- **Source note**: Reseed feedback.
- **Evidence class**: observational
- **Disposition**: venture-ruling
- **Outcome**: Argued ruling appended to WG-WEB-001, now at `archive/v1-final:doctrine/web-design/wargames/WG-WEB-001-surface-register.md`. One argued ruling from one venture, so it is not yet promotion evidence; the philosophy question it raises is carried by `packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md`.
- **Scope**: estate
- **Applies when**: Brands with a print-native or institutional register. One argued ruling from one venture, which under the ladder in GOVERNANCE.md is short of promotion evidence.
- **Informs**: WG-WEB-001, packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md
- **Decided**: 2026-07

### LES-0008 · Ancestry tables need preserved rows, not only compiled ones

- **Lesson**: Reseeds meet pre-EOS files; the ancestry table needs normalised and preserved row kinds beyond compiled and authored.
- **Origin**: harvest
- **Venture**: Venture A
- **Source note**: Reseed feedback.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Default changed: `kernel/templates/COMPILE_REPORT.tpl.md` documents both kinds.
- **Scope**: eos-internal
- **Applies when**: Compiling into a repository that predates the template being compiled.
- **Informs**: kernel/templates/COMPILE_REPORT.tpl.md
- **Decided**: 2026-07

### LES-0009 · A slot pattern that excludes digits lets a slot ship unfilled

- **Lesson**: A slot pattern that excludes digits lets a digit-bearing slot ship unfilled through a green seed check.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: Cold-start probe.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: Bug fixed: E008's `SLOT_RE` in `tools/eos/checks/structural.py` widened to `[A-Z0-9_]+`, with a regression test. `{{SUCCESS_90}}` in `kernel/templates/VENTURE_BRIEF.tpl.md` was the live instance.
- **Scope**: eos-internal
- **Applies when**: Any checker matching template slots by pattern, where a slot name may carry digits.
- **Informs**: tools/eos/checks/structural.py, kernel/templates/VENTURE_BRIEF.tpl.md
- **Decided**: 2026-08

### LES-0010 · A checker that walks every file trips on vendored trees

- **Lesson**: A checker that walks every markdown file under the seed path fails on vendored dependency trees.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: S1.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: Already fixed in v2: `SKIP_DIRS` in `tools/eos/repo.py` skips `node_modules`, `.git`, `__pycache__` and `.pytest_cache`. Recorded as confirmation that the v2 rewrite closed it.
- **Scope**: eos-internal
- **Applies when**: Ventures whose repository carries vendored dependency trees under the seed path.
- **Informs**: tools/eos/repo.py
- **Decided**: 2026-08

### LES-0011 · A two-edit claim protocol lets two launchers collide

- **Lesson**: A claim protocol where the queue row and the claim are two edits lets two launchers collide on one item.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: S1.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: Fixed by design in v2: claims are coordinator-assigned and committed before dispatch, and lanes never acquire or mutate one (`kernel/schemas/claims.schema.json`).
- **Scope**: eos-internal
- **Applies when**: Any queue where more than one session can start work at the same time.
- **Informs**: kernel/schemas/claims.schema.json
- **Decided**: 2026-08

### LES-0013 · A cold-start probe finds defects a warm session cannot see

- **Lesson**: A cold-start probe run before the human rubric is signed surfaces real defects a warm session cannot see.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: S1.
- **Evidence class**: observational
- **Disposition**: venture-ruling
- **Outcome**: Promotion candidate for PB-E04. One argued ruling from one venture, so not yet binding evidence. The drill apparatus is the natural home: all twenty-two drills now carry scenarios and graders, and ADR-0007 defers running them, so nothing has graded this.
- **Scope**: eos-internal
- **Applies when**: A venture at Session 0 whose rubric is not yet signed, probed by a session with no prior context of the repository.
- **Informs**: PB-E04
- **Decided**: 2026-08

### LES-0015 · Local-first PWA with a WASM core is a distinct proven shape

- **Lesson**: A local-first browser product with a WASM compute core is a distinct proven shape, not a bend of the fullstack profile.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: S1.
- **Evidence class**: observational
- **Disposition**: dated-registry-fact
- **Outcome**: Registry addition: `registry/stacks/STACK-local-first-pwa.md`, carrying S1's worked evidence and five sharp edges.
- **Scope**: estate
- **Applies when**: A browser-delivered product whose data stays on the operator's machines and whose compute is latency-sensitive. Where the data may leave the machine, the fullstack profile is the cheaper shape.
- **Informs**: registry/stacks/STACK-local-first-pwa.md
- **Decided**: 2026-08
- **Review**: 2027-02

### LES-0016 · Platform-native deployment beats containers on a sovereign LAN

- **Lesson**: Platform-native deployment beats the container default on a sovereign LAN with no parity or handover trigger.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: WG-OPS-002 ruled contrary.
- **Evidence class**: observational
- **Disposition**: venture-ruling
- **Outcome**: Contrary evidence recorded against the container default. Under `GOVERNANCE.md` precedence this triggers review, never automatic demotion, and one ruling from one venture is not promotion evidence. Carried to `packs/devops-reliability` at the next authoring pass.
- **Scope**: estate
- **Applies when**: Deployment onto machines the operator owns, on a LAN, with no environment-parity requirement and no handover to another operator.
- **Informs**: packs/devops-reliability/PACK.md
- **Conflicts with**: WG-OPS-002
- **Conflict resolutions**: WG-OPS-002: resolution: scoped-differently; note: The container default holds where environment parity or a handover to another operator is in play; this ruling covers a sovereign LAN with neither.
- **Decided**: 2026-08

### LES-0017 · A split voice register reads cleanly in practice

- **Lesson**: A split voice register, warm-guide for in-app coaching and peer-expert for docs, reads cleanly in practice.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: WG-VOX-001 ruled split.
- **Evidence class**: observational
- **Disposition**: venture-ruling
- **Outcome**: Early supporting evidence for the three-way voice scope in `packs/writing-content/guides/GD-WRIT-003-voice-scope.md`, which already sanctions per-surface splits.
- **Scope**: estate
- **Applies when**: Products carrying both in-app coaching copy and reference documentation, where one register would have to serve both.
- **Informs**: packs/writing-content/guides/GD-WRIT-003-voice-scope.md
- **Decided**: 2026-08

### LES-0025 · Local-first is seven ideals, and a product names the subset it buys

- **Lesson**: Offline capability is one of the seven local-first ideals and not the load-bearing one: multi-device, collaboration, longevity, security and privacy, user control and no-spinners drive most of the architecture. A product that keeps its data on the operator's machines should name the subset it is buying and the ones it is declining, because shipped systems treat the list as a menu. A sync engine that narrowed itself to the read path and left writes to the application is the worked case: most of the benefit, a fraction of the cost.
- **Origin**: study
- **Evidence**: EV-0378, EV-0382
- **Lens**: LENS-0001
- **Source note**: First worked instance of the Study workflow, written on 2026-08-10 during the v2.1 build over material already in the tree: the lens was recorded over the 2026-08-08 harvest and no new source was read. The reasoning line is this build's, not Daniel's. LENS-0001 is the id reserved for the contract file, and on the day this row was decided no such file existed in this repository: the estate names no path for an EOS-side lens contract, and `kernel/templates/LENS.tpl.md` sends a venture's to `docs/lenses/`.
- **Evidence class**: observational
- **Disposition**: reference-only
- **Outcome**: Nothing changed. The row records the argument behind the shape already in `registry/stacks/STACK-local-first-pwa.md`, which was harvested at LES-0015 and states the shape without stating which ideals it buys.
- **Scope**: estate
- **Applies when**: A local-first or browser-delivered product deciding how much sync to build. The primary source is a 2019 position paper by CRDT authors with a stake in the answer and no measurement behind it, so it argues the shape of the decision rather than settling it.
- **Informs**: registry/stacks/STACK-local-first-pwa.md, LES-0015
- **Decided**: 2026-08-10
- **Reasoning**: The profile already carried the shape; what it lacked was the argument for which ideals a machine-local product actually buys.
- **Review**: 2027-02

## Rejected

### LES-0001 · Hydration warnings are often browser-extension noise

- **Lesson**: Hydration warnings are often browser-extension noise; verify in a clean profile before treating one as a bug.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Recorded at EOS creation as "Lesson row only, declined as doctrine (too narrow)".
- **Evidence class**: anecdotal
- **Disposition**: rejected
- **Outcome**: Declined. No guide id and no evidence row, on purpose.
- **Scope**: estate
- **Applies when**: Browser applications reporting hydration or client-render mismatches in development.
- **Decided**: 2026-07
- **Reasoning**: Too narrow to bind, and no pack owns it.

## Deferred

No deferred rows.

## Pruned

### LES-0012 · Inception necessarily writes to main

- **Lesson**: Inception necessarily writes to main, because the org that mandates branches is being compiled during the writes.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: S1.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: Deferred at the harvest and queued as T-0005. That task closed on 2026-08-11: `inception/INCEPTION.md` states the Session 0 write-to-main exemption under its own heading, so the first review session no longer reads Session 0's history as a violation.
- **Scope**: eos-internal
- **Applies when**: Session 0 in a fresh venture repository, before the branch rule it is compiling exists.
- **Informs**: inception/INCEPTION.md, T-0005
- **Decided**: 2026-08-11
- **Pruned**: 2026-08-11

### LES-0014 · Doctrine-heavy ventures walk long at Session 0

- **Lesson**: A venture whose master prompt fixes deep product doctrine walks long at Session 0, because doctrine engages triggers the interview leaves silent.
- **Origin**: harvest
- **Venture**: Guth
- **Source note**: S1, 32 rulings against a 20 budget.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: Deferred at the harvest and queued as T-0006. That task closed on 2026-08-11: `inception/WALK_ORDER.md` budgets interview-triggered and doctrine-triggered rulings separately, so a correct doctrine-heavy walk no longer reads as an overrun.
- **Scope**: eos-internal
- **Applies when**: Ventures arriving with fixed product doctrine already in the master prompt.
- **Informs**: inception/WALK_ORDER.md, T-0006
- **Decided**: 2026-08-11
- **Pruned**: 2026-08-11

### LES-0018 · Cap urllib3 below 2.5 until a deploy proves otherwise

- **Lesson**: urllib3 2.5 and above breaks Railway startup; cap it below 2.5.0 until a deploy proves otherwise.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: dated-registry-fact
- **Outcome**: Now owned by `registry/stacks/STACK-fastapi-postgres.md`.
- **Scope**: estate
- **Applies when**: Python services on the FastAPI and Postgres profile deploying to Railway.
- **Informs**: registry/stacks/STACK-fastapi-postgres.md
- **Decided**: 2026-07
- **Review**: 2027-01
- **Pruned**: 2026-08-03

### LES-0019 · Dockerignore node_modules or Windows pnpm symlinks break the build

- **Lesson**: Docker builds on Windows fail on pnpm symlinks unless every node_modules directory is dockerignored.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: dated-registry-fact
- **Outcome**: Now owned by `registry/stacks/STACK-fullstack-app.md`.
- **Scope**: estate
- **Applies when**: Docker builds run on a Windows host in a pnpm workspace.
- **Informs**: registry/stacks/STACK-fullstack-app.md
- **Decided**: 2026-07
- **Review**: 2027-01
- **Pruned**: 2026-08-03

### LES-0020 · Generated artefacts need a drift check or they rot

- **Lesson**: Generated artefacts, OpenAPI types and schemas among them, must be committed with a CI drift check, or they rot silently.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Now owned by `packs/architecture/PACK.md` and its CHECKS row, argued in WG-ARCH-005.
- **Scope**: estate
- **Applies when**: Any repository committing generated artefacts alongside the source they are generated from.
- **Informs**: packs/architecture/PACK.md, WG-ARCH-005
- **Decided**: 2026-07
- **Pruned**: 2026-08-03

### LES-0021 · Visual regression needs a pinned image or fonts diverge

- **Lesson**: Visual regression needs a Docker-pinned image or fonts diverge across machines.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Now owned by `packs/delivery-testing/PACK.md`, argued in WG-DEL-003.
- **Scope**: estate
- **Applies when**: Test suites comparing rendered screenshots across machines.
- **Informs**: packs/delivery-testing/PACK.md, WG-DEL-003
- **Decided**: 2026-07
- **Pruned**: 2026-08-03

### LES-0022 · Migrations: forward-only, idempotent, advisory-locked

- **Lesson**: Migrations: forward-only, idempotent, advisory-locked, run before app start, fail closed.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Now owned by `packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md`.
- **Scope**: estate
- **Applies when**: Relational schema changes shipped with the application that reads them.
- **Informs**: packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md
- **Decided**: 2026-07
- **Pruned**: 2026-08-03

### LES-0023 · Ratcheting gates beat big-bang strictness

- **Lesson**: Ratcheting gates, a mypy allowlist and coverage floors among them, beat big-bang strictness.
- **Origin**: harvest
- **Venture**: WiseWattage
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Now owned by `packs/delivery-testing/refs/QUALITY_SIGNALS.md` and its CHECKS rows.
- **Scope**: estate
- **Applies when**: Tightening quality gates on a codebase that does not pass them yet.
- **Informs**: packs/delivery-testing/refs/QUALITY_SIGNALS.md
- **Decided**: 2026-07
- **Pruned**: 2026-08-03

### LES-0024 · The prune-and-fill compile is mechanical enough to script

- **Lesson**: The prune-and-fill compile is mechanical enough to script; twenty lines compiled the two largest files with zero manual fixes.
- **Origin**: harvest
- **Venture**: Venture A
- **Source note**: Reseed feedback.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: Now owned by `inception/INCEPTION.md` phase D.
- **Scope**: eos-internal
- **Applies when**: Compiling kernel templates into a venture repository where the fill values are already known.
- **Informs**: inception/INCEPTION.md
- **Decided**: 2026-07
- **Pruned**: 2026-08-03
