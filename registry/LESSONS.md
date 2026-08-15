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

**Live: 50. Rejected: 3. Deferred: 2. Pruned: 9.** A rejected row
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
more, because binding needs an accepted ADR and the operator under the
ladder in `GOVERNANCE.md`.

**A lesson leaves this ledger once its content is stated as a rule
somewhere else.** Keeping it here as well would be a second home for
the same rule, and one of the two homes would go stale. Rows that
record what changed and why are provenance, and those stay.

The first PB-E02 harvest ran on 2026-08-08 against the three governed
ventures. Venture A's two entries had both already been folded during
the v1 build and are recorded as such below. Venture C's feedback file
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
of binding-candidate. Venture C's five draft wargames stay candidates
for the same reason: a fork that happened once is not a recurring fork,
and a guide written for it would be speculation with a filename.

## Live

### LES-0002 · Plan and build decouple, and nothing in the build is generative

- **Lesson**: Plan and build decouple: agent-driven planning, a deterministic byte-stable build, nothing generative in the build step.
- **Origin**: harvest
- **Venture**: Venture D
- **Source note**: Recorded at EOS creation against Venture D under the repository name it carried then, and corrected to its current name in the v2 pass on 2026-08-03.
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
- **Venture**: Venture B
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
- **Outcome**: WG-WEB-013 filed by the operator, now at `archive/v1-final:doctrine/web-design/wargames/WG-WEB-013-kit-escape-and-enforcement.md`, and carried into `packs/ui-ux/guides/GD-UIUX-004-token-source.md`.
- **Scope**: estate
- **Applies when**: Products with a design system whose tokens are enforced somewhere other than the code that consumes them.
- **Informs**: GD-UIUX-004, packs/ui-ux/guides/GD-UIUX-004-token-source.md
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
- **Informs**: GD-UIUX-001, packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md
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
- **Venture**: Venture C
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
- **Venture**: Venture C
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
- **Venture**: Venture C
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
- **Venture**: Venture C
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
- **Venture**: Venture C
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
- **Venture**: Venture C
- **Source note**: The archived WG-OPS-002 ruled contrary.
- **Evidence class**: observational
- **Disposition**: venture-ruling
- **Outcome**: Contrary evidence against the archived WG-OPS-002 container default. The active dated default lives in `registry/stacks/STACK-fastapi-postgres.md`; this row records the sovereign-LAN exception and does not promote a new estate Doctrine.
- **Scope**: estate
- **Applies when**: Deployment onto machines the operator owns, on a LAN, with no environment-parity requirement and no handover to another operator.
- **Informs**: registry/stacks/STACK-fastapi-postgres.md
- **Conflicts with**: registry/stacks/STACK-fastapi-postgres.md
- **Conflict resolutions**: registry/stacks/STACK-fastapi-postgres.md: resolution: scoped-differently; note: The container default holds where environment parity or a handover to another operator is in play; this ruling covers a sovereign LAN with neither.
- **Decided**: 2026-08

### LES-0017 · A split voice register reads cleanly in practice

- **Lesson**: A split voice register, warm-guide for in-app coaching and peer-expert for docs, reads cleanly in practice.
- **Origin**: harvest
- **Venture**: Venture C
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
- **Source note**: First worked instance of the Study workflow, written on 2026-08-10 during the v2.1 build over material already in the tree: the lens was recorded over the 2026-08-08 harvest and no new source was read. The reasoning line is this build's, not the operator's. LENS-0001 is the id reserved for the contract file, and on the day this row was decided no such file existed in this repository: the estate names no path for an EOS-side lens contract, and `kernel/templates/LENS.tpl.md` sends a venture's to `docs/lenses/`.
- **Evidence class**: observational
- **Disposition**: reference-only
- **Outcome**: Nothing changed. The row records the argument behind the shape already in `registry/stacks/STACK-local-first-pwa.md`, which was harvested at LES-0015 and states the shape without stating which ideals it buys.
- **Scope**: estate
- **Applies when**: A local-first or browser-delivered product deciding how much sync to build. The primary source is a 2019 position paper by CRDT authors with a stake in the answer and no measurement behind it, so it argues the shape of the decision rather than settling it.
- **Informs**: registry/stacks/STACK-local-first-pwa.md, LES-0015
- **Decided**: 2026-08-10
- **Reasoning**: The profile already carried the shape; what it lacked was the argument for which ideals a machine-local product actually buys.
- **Review**: 2027-02

### LES-0026 · Representative measurement precedes a material tool or capacity claim

- **Lesson**: A performance, capacity or tool claim is useful only when its baseline, representative input or workload, acceptance measure and relevant environment are named together. Maintainer examples can identify mechanisms, but they do not set a universal threshold.
- **Origin**: study
- **Evidence**: EV-0566, EV-0568, EV-0570, EV-0573, EV-0574, EV-0578
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Accepted for integration as one scoped Doctrine under the existing data surface, with every compute Wargame linked to it.
- **Scope**: estate
- **Applies when**: A material performance, capacity, engine or acceleration claim. An exploratory spike may use a cheaper sample when it records how that sample differs from the target workload.
- **Informs**: packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: The sources agree that workload, execution mode, compilation, memory and user objective change the answer, while none supplies a universal winner.

### LES-0027 · Data compute uses a measured promotion ladder, not a timeless tool winner

- **Lesson**: The durable default is to keep the highest-level sufficient representation, preserve an ecosystem contract where it matters, profile before acceleration, and distribute only on demonstrated pressure. Package names and versions belong in a dated profile.
- **Origin**: study
- **Evidence**: EV-0566, EV-0567, EV-0568, EV-0569, EV-0570, EV-0571, EV-0572, EV-0573, EV-0574
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Accepted as a scoped Doctrine plus a dated local-tabular stack profile under data analytics; no package name becomes timeless Doctrine.
- **Scope**: estate
- **Applies when**: New local analytical and numerical work where the venture can run a representative comparison and has not already made pandas, an array ABI, SQL, GPU execution or a distributed engine part of its contract.
- **Informs**: packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: The tools expose materially different semantics and operational surfaces, and the Numba CUDA move demonstrates why a package route cannot be a timeless rule.

### LES-0028 · Native semantic HTML is the default, and custom interaction earns its tests

- **Lesson**: Use native HTML semantics and behaviour first. ARIA or a custom interaction must name the missing native capability and carry keyboard, focus and assistive-technology evidence proportionate to the claim.
- **Origin**: study
- **Evidence**: EV-0027, EV-0576, EV-0577
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Accepted for integration as one scoped Doctrine under UI and UX, linked to the custom-interaction Wargame and existing accessibility assurance.
- **Scope**: estate
- **Applies when**: Browser interfaces and embedded web surfaces. A canvas, spatial editor or specialised control may depart where native controls cannot express the task and an accessible alternative or equivalent behaviour is proved.
- **Informs**: packs/ui-ux/PACK.md, GD-UIUX-003
- **Decided**: 2026-08-15
- **Reasoning**: The standards make native semantics the cheaper starting point and make clear that adding a role does not add its required behaviour.

### LES-0029 · Interface philosophy follows users, tasks, devices and failure cost

- **Lesson**: An interface default is selected per surface from its users, tasks, devices, modes and failure cost. A house aesthetic remains an opt-in preference subordinate to accessibility, measured performance and task success.
- **Origin**: study
- **Evidence**: EV-0575, EV-0027
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Merged into the existing design-philosophy Wargame and normalised Doctrine rather than authored as a second visual rule.
- **Scope**: estate
- **Applies when**: Every user-facing surface. Brand preferences activate only through explicit adoption and cannot override accessibility or target-device evidence.
- **Informs**: GD-UIUX-001, packs/ui-ux/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: The W3C Note supports a user-first philosophy but is not a conformance standard, so the rule remains a scoped default rather than a binding aesthetic.

### LES-0030 · One deployable remains the default until a measured split pressure earns distribution

- **Lesson**: Distribution is an operating cost, not a maturity badge. Start with one deployable and enforced internal boundaries, then split only when change coupling, isolation, ownership, capacity or deployment evidence identifies a stable seam.
- **Origin**: study
- **Evidence**: EV-0151, EV-0152, EV-0153
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Linked to the existing architecture Doctrine and deployment-shape procedures; no duplicate monolith rule was admitted.
- **Scope**: estate
- **Applies when**: A new deployable or an existing system considering a service split. Regulatory, isolation, capacity and independent ownership pressure can earn an earlier split.
- **Informs**: packs/architecture/PACK.md, GD-ARCH-001, WG-ARCH-001
- **Decided**: 2026-08-15
- **Reasoning**: Existing EOS evidence already settles the default and its exceptions, while the retained source set adds no independent outcome evidence that warrants another rule.

### LES-0031 · Small, reversible and evidenced are separate change properties

- **Lesson**: A small change can still be irreversible, and a spike can become production by copying or prolonged use. Exploratory work therefore names its deletion or promotion boundary, while retained work takes verification proportionate to risk.
- **Origin**: study
- **Evidence**: EV-0153, EV-0403, EV-0579
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Merged into existing discovery and test-timing guidance, with a relation between reversibility and the spike-to-hardened boundary.
- **Scope**: estate
- **Applies when**: Exploratory changes, vertical slices and normal delivery. Consequential or difficult-to-reverse effects earn stronger evidence even when the diff is small.
- **Informs**: GD-DISC-001, WG-DEL-007
- **Decided**: 2026-08-15
- **Reasoning**: The source sharpens a boundary already present in EOS and does not justify a second general delivery rule.

### LES-0032 · Reliability starts from user journeys, objectives and proved restoration

- **Lesson**: Reliability has three independently reviewable parts: user journeys select indicators, objectives govern change, and persistent data earns a demonstrated restoration path. A database restore alone does not prove service recovery.
- **Origin**: study
- **Evidence**: EV-0096, EV-0201, EV-0203, EV-0578
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Merged into three existing reliability atoms and their procedures rather than one compound Doctrine.
- **Scope**: estate
- **Applies when**: A user-facing or data-bearing service. Safety and integrity floors remain non-spendable even when an error-budget policy permits ordinary reliability trade-offs.
- **Informs**: GD-DEVOPS-003, GD-DEVOPS-004, WG-OPS-003
- **Decided**: 2026-08-15
- **Reasoning**: The propositions activate under different conditions and would become harder to challenge if collapsed into one broad reliability statement.

### LES-0033 · Security assurance is shaped by threats without weakening protected floors

- **Lesson**: Security assurance states the protected property, threat surface and required outcome before selecting controls. Risk tailoring cannot waive an already binding privacy, authorisation, integrity or consequential-action floor.
- **Origin**: study
- **Evidence**: EV-0037, EV-0223, EV-0549
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: Normalised the existing threat-shaped rule and retained the binding security floors; domain disputes route to Wargames.
- **Scope**: estate
- **Applies when**: Security and supply-chain assurance decisions after applicable statutory, privacy, authorisation, integrity and human-approval floors have been identified.
- **Informs**: packs/security-privacy/PACK.md, GD-SEC-003
- **Decided**: 2026-08-15
- **Reasoning**: SSDF supports outcome and risk tailoring, while SLSA's own threat model shows that assurance schemes leave explicit non-goals.

### LES-0034 · Use the simplest agent topology that meets the task

- **Lesson**: Start with one bounded agent and a strong oracle. Add topology only when task decomposability, context isolation, restartability, tool load and verifier placement show that coordination buys more than it costs.
- **Origin**: study
- **Evidence**: EV-0052, EV-0088, EV-0452
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: controlled
- **Disposition**: estate-default
- **Outcome**: Refreshed the evidence behind the existing agent and swarm topology procedures; no second swarm Doctrine was admitted.
- **Scope**: estate
- **Applies when**: Agentic work with a stable task set and an external oracle. The paper's benchmark magnitudes do not transfer as universal thresholds to repository engineering.
- **Informs**: GD-AGENT-001, GD-SWARM-001
- **Decided**: 2026-08-15
- **Reasoning**: Version 3 shows large gains and large losses under different task structures, which supports a Wargame and rejects a universal swarm preference.

### LES-0035 · An evaluation result names the tested system, harness, budget and oracle

- **Lesson**: A model name is not an evaluation description. The result identifies the tested version, task set, harness, tools, budget, scorer, oracle, sampling and conditions needed to reproduce or challenge the claim.
- **Origin**: study
- **Evidence**: EV-0007, EV-0087, EV-0250, EV-0251, EV-0452
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: controlled
- **Disposition**: estate-default
- **Outcome**: Merged into existing evaluation-harness, judge and oracle procedures; no new procedure was admitted because the current routes own the pressure.
- **Scope**: estate
- **Applies when**: Any comparative model, agent, retrieval or automated-evaluation claim used to select or govern a system.
- **Informs**: GD-AIML-001, GD-AIML-003, GD-AGENT-004, WG-DEL-006
- **Decided**: 2026-08-15
- **Reasoning**: The apparent effect can change with model family, task graph, tool load and verifier placement, so those facts must travel with the result.

### LES-0037 · Analytical engine choice is a measured workload decision

- **Lesson**: Polars, pandas, DuckDB and Spark solve overlapping but different jobs. Engine selection records semantic fit, ecosystem contract, wall time, peak memory or spill, operating surface and integration cost on one representative pipeline.
- **Origin**: study
- **Evidence**: EV-0566, EV-0567, EV-0568, EV-0572, EV-0573, EV-0574
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new analytical engine-selection Wargame under the existing data surface; it may share an advanced procedure with execution mode if both rulings stay separate.
- **Scope**: estate
- **Applies when**: A local or distributed analytical workload choosing or materially changing its dataframe or SQL execution engine.
- **Informs**: packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: No engine is an unconditional winner, and the cheapest useful discriminator is a representative pipeline under a shared correctness oracle.

### LES-0038 · Representation movement is an architectural boundary

- **Lesson**: A dataframe-to-array or solver boundary names dtype, layout, device, copy behaviour, ownership, peak memory, transfer cost and numerical tolerance. Interoperability support does not make those properties implicit.
- **Origin**: study
- **Evidence**: EV-0568, EV-0569
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new representation-boundary Wargame under the existing data surface.
- **Scope**: estate
- **Applies when**: A dataframe, array, solver or device boundary where representation movement can affect memory, performance or correctness.
- **Informs**: packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: A representative round trip can expose copies, type changes and tolerance failures before the boundary becomes difficult to reverse.

### LES-0039 · Acceleration is earned by a measured hotspot and a numerical oracle

- **Lesson**: Choose among vectorised NumPy, Numba, native code and GPU execution only after profiling the same hotspot. Compare compile-inclusive first use and steady state, and record any parallel, device or floating-point change separately.
- **Origin**: study
- **Evidence**: EV-0569, EV-0570, EV-0571
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new acceleration Wargame under the existing data surface; current package routes remain dated stack facts.
- **Scope**: estate
- **Applies when**: A measured numerical hotspot whose cost matters to the stated objective and whose correctness can be compared under explicit tolerances.
- **Informs**: packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Compilation, unsupported features, device transfer and relaxed arithmetic can remove or reverse an apparent speed gain.

### LES-0040 · Execution mode trades visibility, memory, ordering and operating cost

- **Lesson**: Eager, lazy, streaming, out-of-core and distributed execution are conditional choices. A ruling records the plan, ordering, peak memory, spill, duration, failure behaviour and reproducibility across clean runs.
- **Origin**: study
- **Evidence**: EV-0566, EV-0573, EV-0574
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted execution mode as a distinct ruling surface, either in its own Wargame or as an independently ruleable part of analytical engine selection.
- **Scope**: estate
- **Applies when**: An analytical pipeline choosing how and where its plan executes, especially when ordering, memory, spill or reproducibility is material.
- **Informs**: packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Out of core is bounded and distribution adds costs, while lazy execution can trade intermediate visibility for optimisation.

### LES-0041 · Web delivery shape follows the route and target device

- **Lesson**: Static, server-rendered, client-rendered, islands, PWA and native delivery should be compared on a representative route for useful content, interaction, navigation, accessibility tree, offline need, cache behaviour and operating complexity.
- **Origin**: study
- **Evidence**: EV-0027, EV-0575
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new web-delivery Wargame under the UI surface, related to the existing native-client architecture procedure without reviving retired web IDs.
- **Scope**: estate
- **Applies when**: A public or internal web surface choosing its primary rendering and delivery architecture, including a comparison with native delivery where device integration is material.
- **Informs**: packs/ui-ux/PACK.md, GD-NAT-001
- **Decided**: 2026-08-15
- **Reasoning**: The current estate has a native-client procedure but no live procedure that owns the complete web-delivery fork.

### LES-0042 · Novice and expert density is already a per-surface design ruling

- **Lesson**: Information density is not a house default. It is selected from representative novice and expert task completion, error and search cost, with progressive disclosure or separate modes where one surface cannot serve both well.
- **Origin**: study
- **Evidence**: EV-0575, EV-0239, EV-0404
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: reference-only
- **Outcome**: Covered by a Doctrine relation to the existing design-philosophy Wargame; no duplicate density procedure was admitted.
- **Scope**: estate
- **Applies when**: A surface used by people with materially different familiarity, frequency or task complexity.
- **Informs**: GD-UIUX-001
- **Decided**: 2026-08-15
- **Reasoning**: The existing procedure already asks the deciding audience, task, session and failure-cost questions.

### LES-0043 · Custom rendering must replace the behaviour native semantics would have supplied

- **Lesson**: Canvas and custom controls are justified only where native semantics cannot express the task. The exception names keyboard, focus, accessibility-tree or equivalent interaction and tests the hardest representative path on relevant browser and assistive-technology pairs.
- **Origin**: study
- **Evidence**: EV-0027, EV-0576, EV-0577
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new semantic-versus-custom-interaction Wargame linked to component sourcing and accessibility assurance.
- **Scope**: estate
- **Applies when**: A browser interaction considering canvas, a custom widget or an ARIA reconstruction because native controls appear insufficient.
- **Informs**: GD-UIUX-002, GD-UIUX-003, packs/ui-ux/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: A role is a promise rather than an implementation, and copied authoring patterns do not prove product behaviour.

### LES-0044 · House style and motion remain subordinate to audience and accessibility

- **Lesson**: House style is an optional adopted preference. Motion and visual treatment yield to audience, task, reduced-motion choice, accessibility floors and measured loading or frame behaviour on target devices.
- **Origin**: study
- **Evidence**: EV-0027, EV-0232, EV-0575
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: reference-only
- **Outcome**: Covered by explicit relations among the existing design, accessibility and house-style procedures; no new Wargame was admitted.
- **Scope**: estate
- **Applies when**: A venture that explicitly adopts PatterTech house style or proposes motion and visual treatments on a user-facing surface.
- **Informs**: GD-UIUX-001, GD-UIUX-003, GD-HOUSE-001
- **Decided**: 2026-08-15
- **Reasoning**: The live procedures already separate optional taste from audience, accessibility and performance evidence.

### LES-0045 · Refresh the monolith-to-services Wargame around measured sensitivities

- **Lesson**: A service split is argued from recent change coupling, deployment cadence, isolation, ownership and capacity. Before splitting deployment, test one proposed seam and record which quality is sensitive to it and what reversal would cost.
- **Origin**: study
- **Evidence**: EV-0151, EV-0152, EV-0153, EV-0564
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Refreshed the existing deployment-shape procedures with forces, affected qualities, sensitivity and reversal fields while preserving their IDs.
- **Scope**: estate
- **Applies when**: A modular monolith considering a service boundary or a distributed system considering consolidation.
- **Informs**: GD-ARCH-001, WG-ARCH-001
- **Decided**: 2026-08-15
- **Reasoning**: ATAM contributes lightweight trade-off structure, while the estate's current evidence already owns the one-deployable default.

### LES-0046 · Message flow is chosen from latency, ordering, retry, consistency and replay

- **Lesson**: Synchronous calls, queues, events and streams make different guarantees. A decision failure-injects one representative operation and observes latency, duplicate handling, ordering, retry, replay and user-visible state.
- **Origin**: study
- **Evidence**: EV-0151, EV-0157, EV-0162, EV-0163
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new messaging-and-flow Wargame in architecture, related to background-work and ingestion procedures.
- **Scope**: estate
- **Applies when**: A boundary choosing its interaction contract where latency, ordering, retries, consistency or replay affects correctness or user experience.
- **Informs**: WG-ARCH-004, GD-DATAENG-001, packs/architecture/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Existing procedures choose background machinery or ingestion shape but do not own the general interaction contract.

### LES-0047 · Storage engines are selected from workload and recovery obligations

- **Lesson**: Transactional, analytical, search, graph, object and time-series storage are not interchangeable labels. Compare a representative read and write trace plus restore or rebuild behaviour against the simplest credible candidates.
- **Origin**: study
- **Evidence**: EV-0150, EV-0162, EV-0572, EV-0573
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new storage-engine Wargame under architecture with data-analytics activation.
- **Scope**: estate
- **Applies when**: A durable data surface choosing or replacing its primary engine or adding a specialised secondary engine.
- **Informs**: WG-ARCH-002, WG-ARCH-008, packs/architecture/PACK.md, packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Current procedures cover access style, topology and analytical storage separately but do not decide engine purpose and recoverability together.

### LES-0048 · Local, hosted, hybrid and offline placement is a consistency decision

- **Lesson**: Placement determines data ownership, outage behaviour and reconciliation. Disconnect during a representative write, reconnect, introduce a concurrent change and measure data loss, conflict visibility and recovery effort.
- **Origin**: study
- **Evidence**: EV-0206, EV-0379, EV-0380, EV-0382
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new locality-and-consistency Wargame under architecture and related it to the existing offline-write procedure.
- **Scope**: estate
- **Applies when**: A system placing state across local devices, hosted services or both, especially where writes continue during disconnection.
- **Informs**: GD-NAT-002, packs/architecture/PACK.md, packs/native-client/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: The native procedure owns client writes but not whole-system placement, data ownership and cross-location consistency.

### LES-0049 · A spike names its deletion, promotion and hardening boundary

- **Lesson**: A spike is safe only while its learning artefact is visibly separated from user-facing software. The narrowest end-to-end path should also list the hardening work required before anything is retained or reaches users.
- **Origin**: study
- **Evidence**: EV-0003, EV-0192, EV-0579
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Refreshed the existing test-timing Wargame and its discovery relation with explicit deletion, promotion and evidence boundaries.
- **Scope**: estate
- **Applies when**: Exploratory work deciding between a disposable spike and a hardened vertical slice.
- **Informs**: WG-DEL-007, GD-DISC-001
- **Decided**: 2026-08-15
- **Reasoning**: A small exploratory artefact can quietly become production, so retention is a separate decision from building it.

### LES-0050 · Test fidelity and oracle independence are linked but distinct

- **Lesson**: Doubles, sandboxes and live boundaries answer fidelity, while an independent oracle answers whether the result is true. Run the same contract at the nearest real boundary and seed one mismatch that the independent oracle must catch.
- **Origin**: study
- **Evidence**: EV-0007, EV-0184, EV-0189, EV-0191
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: controlled
- **Disposition**: decision-guide
- **Outcome**: Refreshed and related the existing test-double and oracle-independence Wargames; no third procedure was admitted.
- **Scope**: estate
- **Applies when**: A test strategy selecting a fake, sandbox or live system and deciding what independent truth will detect contract drift or a mutually consistent defect.
- **Informs**: WG-DEL-005, WG-DEL-006
- **Decided**: 2026-08-15
- **Reasoning**: A high-fidelity boundary can share the same mistaken expectation, and an independent oracle can still operate against a lower-fidelity double.

### LES-0051 · An incident hotfix is a narrower gate, not no gate

- **Lesson**: Urgent mitigation assesses and observes user impact before root-cause work, keeps supervision, a known-good state and rollback, and preserves every non-waivable safety check. The incident route is proved with a timed apply-and-rollback drill.
- **Origin**: study
- **Evidence**: EV-0423, EV-0580
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new incident-hotfix versus normal-gate Wargame under delivery and reliability.
- **Scope**: estate
- **Applies when**: A declared incident where waiting for the normal delivery path causes greater user harm, and a rollback or known-good recovery route exists.
- **Informs**: packs/delivery-testing/PACK.md, packs/devops-reliability/PACK.md, GD-DEVOPS-002
- **Decided**: 2026-08-15
- **Reasoning**: Existing release controls assume normal delivery, while incident practice supports mitigation first without supporting an unbounded bypass.

### LES-0052 · Capability ownership includes portability and incident access

- **Lesson**: Build, buy and managed-service decisions include who can diagnose an outage, export state and restore service, not only feature fit and purchase cost. Exercise outage, export and restore before relying on the provider boundary.
- **Origin**: study
- **Evidence**: EV-0069, EV-0161
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new capability-ownership Wargame in architecture with supply-chain relations.
- **Scope**: estate
- **Applies when**: A material capability choosing between owned implementation, purchased software or a managed service, especially where provider failure can block diagnosis or recovery.
- **Informs**: WG-ARCH-007, GD-SUPPLY-004, packs/architecture/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Vendor seams and code vendoring do not by themselves decide capability ownership or prove incident access.

### LES-0053 · Degrade honestly only while protected properties still hold

- **Lesson**: Graceful degradation preserves a named minimum useful journey, reports its state truthfully and keeps monitoring and a kill switch. It is disqualified where the reduced path weakens privacy, authorisation, integrity or consequential-action approval.
- **Origin**: study
- **Evidence**: EV-0225, EV-0581
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new fail-closed versus honest-degradation Wargame under reliability with security activation and protected-set disqualifiers.
- **Scope**: estate
- **Applies when**: A dependency or subsystem failure where some useful service might continue without weakening a protected property.
- **Informs**: packs/devops-reliability/PACK.md, packs/security-privacy/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: The reliability source supports simple exercised degradation, while protected-set rules make fail-closed behaviour non-negotiable for specific properties.

### LES-0054 · Observability must prove diagnostic value and data minimisation together

- **Lesson**: Telemetry is sufficient only when it can diagnose a representative seeded incident without exposing secrets, unnecessary personal data or cross-tenant context. More collection is not a substitute for a better diagnostic model.
- **Origin**: study
- **Evidence**: EV-0021, EV-0225
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new observability-and-privacy Wargame under reliability with security activation.
- **Scope**: estate
- **Applies when**: A service adding or changing logs, traces, metrics or diagnostic event capture where records can contain personal, secret or tenant-specific context.
- **Informs**: packs/devops-reliability/PACK.md, packs/security-privacy/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Observability is an uncovered estate capability and privacy constrains the same records, so leaving the tension implicit is high consequence.

### LES-0055 · Provenance proves production facts, not producer trust or artefact safety

- **Lesson**: A valid attestation can establish where, when and how an artefact was produced within its trust model. It cannot establish benign producer intent, product correctness, safe dependencies or safe use.
- **Origin**: study
- **Evidence**: EV-0038, EV-0549, EV-0582
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Refreshed the existing provenance Wargame and added the relation between verified provenance and separate producer and dependency admission.
- **Scope**: estate
- **Applies when**: Admission or deployment of an artefact carrying provenance, an SBOM or both.
- **Informs**: GD-SUPPLY-001
- **Decided**: 2026-08-15
- **Reasoning**: The SLSA provenance and threat pages state different assurance surfaces and explicit non-goals, so attestation cannot be used as a safety proxy.

### LES-0056 · Dependency freshness and known-good deployment are one governed tension

- **Lesson**: A newer dependency can close a known security exposure and can also replace a proven deployment with an unobserved one. A security-fix exception still takes the suite, staged observation, rollback and incident-reconstruction path proportionate to consequence.
- **Origin**: study
- **Evidence**: EV-0038, EV-0069, EV-0204, EV-0549
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Refreshed and related the existing dependency-cadence and release-control Wargames; no duplicate update procedure was admitted.
- **Scope**: estate
- **Applies when**: A dependency update, especially an urgent security update, where the currently deployed version is known good and the replacement is not yet observed in production shape.
- **Informs**: GD-SUPPLY-003, GD-DEVOPS-002
- **Decided**: 2026-08-15
- **Reasoning**: Freshness and deployment confidence are separate assurance axes, and neither should silently erase the other.

### LES-0057 · Agent topology compares against one bounded single-agent control

- **Lesson**: A deterministic workflow, single agent and multi-agent topology are compared on the same frozen task set, model budget, tools and external verifier. Tool load and central verification are first-class pressures, not after-the-fact explanations.
- **Origin**: study
- **Evidence**: EV-0052, EV-0088, EV-0452
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: controlled
- **Disposition**: decision-guide
- **Outcome**: Refreshed the existing topology Wargames with version 3 evidence, tool-load pressure and central-verification checks.
- **Scope**: estate
- **Applies when**: Agentic work considering topology beyond a direct bounded agent or replacing deterministic orchestration with an agent loop.
- **Informs**: GD-AGENT-001, GD-SWARM-001
- **Decided**: 2026-08-15
- **Reasoning**: The controlled study shows topology effects reverse with task structure, so the baseline and harness must remain fixed during comparison.

### LES-0058 · Model hosting is a data-route, device-capacity and outage decision

- **Lesson**: Local, hosted and hybrid inference are compared on the same frozen evaluation set for quality, latency, cost, data movement and recovery under provider or network loss. A model name alone does not settle hosting.
- **Origin**: study
- **Evidence**: EV-0245, EV-0258, EV-0259, EV-0260, EV-0261, EV-0262
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: decision-guide
- **Outcome**: Admitted a new model-hosting Wargame under AI and ML, related to the existing model-lifecycle procedure.
- **Scope**: estate
- **Applies when**: An AI feature deciding whether inference runs on the target device, through a provider or across a hybrid fallback path.
- **Informs**: GD-AIML-005, packs/ai-ml-llm/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: The live model-choice procedure covers cost and retirement but not inference locality, data route, device capacity or provider outage.

### LES-0059 · Use deterministic judges where truth is decidable and calibrate the rest

- **Lesson**: Deterministic scoring comes first where correctness is decidable. Human and model judges are calibrated against the same labelled sample, with agreement, disagreement, order effects, abstention and cost reported.
- **Origin**: study
- **Evidence**: EV-0007, EV-0250, EV-0251, EV-0252, EV-0253, EV-0254
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: controlled
- **Disposition**: decision-guide
- **Outcome**: Refreshed and related the existing judge-selection and oracle-independence Wargames; no new judge procedure was admitted.
- **Scope**: estate
- **Applies when**: An evaluation choosing deterministic, human or model scoring for an output that affects acceptance or comparison.
- **Informs**: GD-AIML-003, WG-DEL-006
- **Decided**: 2026-08-15
- **Reasoning**: Judge families can share error and self-preference with the system under test, so calibration and independence are part of the result.

### LES-0061 · Local exceptions do not become Doctrine without repeated evidence

- **Lesson**: A venture ruling is local authority. Promotion requires overlapping argued cases, generalisability evidence and the existing governance ladder; a new Wargame would create a competing promotion route.
- **Origin**: study
- **Evidence**: EV-0537, EV-0097
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: asserted
- **Disposition**: reference-only
- **Outcome**: Covered by Doctrine-to-ruling and promotion-evidence relations under the existing governance path; no new Wargame was admitted.
- **Scope**: estate
- **Applies when**: A local ruling appears to contradict or improve a default and somebody proposes applying it beyond the venture that made it.
- **Informs**: GOVERNANCE.md, ADR-0014
- **Decided**: 2026-08-15
- **Reasoning**: The cited research-control evidence supports recording counter-evidence and decisions. The operator-approved governance ladder, not an external platform source, supplies the promotion threshold.

### LES-0064 · One advanced Wargame form carries lifecycle, trade-offs and interaction coverage

- **Lesson**: A Wargame starts from a decision question and stakes, exposes forces, affected qualities and sensitivities, plans discriminating evidence, and records constraints and interactions only where they change the ruling. Interaction coverage still needs a valid parameter model and oracle.
- **Origin**: study
- **Evidence**: EV-0563, EV-0564, EV-0565
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: implementation-reference
- **Outcome**: The unified Wargame schema, authoring contract and semantic checks use one advanced form across stable GD and WG identities.
- **Scope**: eos-internal
- **Applies when**: New and refreshed EOS Wargames. Defence ceremony, full ATAM workshops and generated covering arrays remain optional and do not transfer as mandatory process.
- **Informs**: kernel/schemas/wargame.schema.json, ADR-0012
- **Decided**: 2026-08-15
- **Reasoning**: The three sources contribute complementary lifecycle, sensitivity and interaction concepts without requiring three scenario types or a larger file count.

## Rejected

### LES-0001 · Hydration warnings are often browser-extension noise

- **Lesson**: Hydration warnings are often browser-extension noise; verify in a clean profile before treating one as a bug.
- **Origin**: harvest
- **Venture**: Venture B
- **Source note**: Recorded at EOS creation as "Lesson row only, declined as doctrine (too narrow)".
- **Evidence class**: anecdotal
- **Disposition**: rejected
- **Outcome**: Declined. No guide id and no evidence row, on purpose.
- **Scope**: estate
- **Applies when**: Browser applications reporting hydration or client-render mismatches in development.
- **Decided**: 2026-07
- **Reasoning**: Too narrow to bind, and no pack owns it.

### LES-0060 · Reject a golden-path Wargame until the estate has a platform consumer

- **Lesson**: A one-operator estate cannot yet distinguish a useful golden path from a compulsory template because no independent consumer can measure adoption, escape cost or recovery from the path's failure.
- **Origin**: study
- **Evidence**: EV-0058, EV-0205
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: asserted
- **Disposition**: rejected
- **Outcome**: No golden-path versus autonomy Wargame was admitted in this programme; existing profiles, seeds and domain Wargames continue to provide optional local defaults.
- **Scope**: estate
- **Applies when**: The estate has one operator and no internal teams consuming a shared platform product.
- **Informs**: registry/coverage.json
- **Decided**: 2026-08-15
- **Reasoning**: Admitting the Wargame now would invent a second governance surface before ADR-0014's second-team trigger has fired.
- **Revisit when**: A second independently operating team consumes a shared platform path and can test completion, failure recovery and escape-route cost.

### LES-0063 · The admitted pressures fit existing packs

- **Lesson**: The web, UI, reliability, supply-chain and AI pressures have live destination packs and cross-pack activation paths. A new pack would add activation and ownership ambiguity before repeated evidence establishes a broader independent capability.
- **Origin**: study
- **Evidence**: EV-0027, EV-0037, EV-0038, EV-0452, EV-0549, EV-0575, EV-0578, EV-0581
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: asserted
- **Disposition**: rejected
- **Outcome**: No new web, UI, reliability, supply-chain or AI pack was admitted; the new and refreshed Wargames land in current packs with relations where ownership crosses domains.
- **Scope**: estate
- **Applies when**: This first pressure tranche, where every admitted decision has an existing owning pack or a clear cross-pack activation route.
- **Informs**: registry/coverage.json
- **Decided**: 2026-08-15
- **Reasoning**: Pack creation is not required to make a pressure visible, and no retained source proves a separate capability boundary for this estate.
- **Revisit when**: A repeated pressure cannot be owned or activated cleanly through any current pack and brings its own evidence, worked example and drill.

## Deferred

### LES-0036 · Defer a platform Doctrine until a second team proves the consumer pressure

- **Lesson**: Golden paths can reduce repeated work and can also rot or suppress valid local choices. The current one-operator estate has no independent platform consumer, so it cannot yet test adoption, failure recovery or escape-route cost.
- **Origin**: study
- **Evidence**: EV-0058, EV-0205
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: asserted
- **Disposition**: deferred
- **Outcome**: No first-class golden-path Doctrine was admitted; platform engineering remains registry-only.
- **Scope**: estate
- **Applies when**: The current estate has one operator and no independent team consuming a shared internal platform. Individual profiles and seeds may still provide optional defaults with tested escapes.
- **Informs**: registry/coverage.json
- **Decided**: 2026-08-15
- **Reasoning**: The approved source set supplies no platform outcome evidence for this estate, and admitting Doctrine now would bypass ADR-0014's consumer trigger.
- **Revisit when**: A second independently operating team consumes a shared platform path and can measure completion, failure recovery, voluntary adoption and escape-route cost.

### LES-0062 · Scientific and reproducible computing has not earned a pack

- **Lesson**: The public source set establishes maintained compute references and a real contradicting implementation choice, but it does not establish two materially distinct executable local examples, a sanitised exemplar, a reviewable drill or a clear admission boundary.
- **Origin**: study
- **Evidence**: EV-0566, EV-0567, EV-0568, EV-0569, EV-0570, EV-0571, EV-0572, EV-0573, EV-0574
- **Lens**: LENS-0002
- **Source note**: The operator's explicit instruction to implement T-0026 authorised this programme disposition; the research report supplied the recommendation, not the authority.
- **Evidence class**: observational
- **Disposition**: deferred
- **Outcome**: Scientific and reproducible computing remains registry-only; dated compute profiles and experimental Wargames stay under the existing data surface.
- **Scope**: estate
- **Applies when**: The current tranche has public documentation but no qualifying local example pair, sanitised exemplar or drill packet.
- **Informs**: registry/coverage.json, packs/data-analytics/PACK.md
- **Decided**: 2026-08-15
- **Reasoning**: Building a pack on source count alone would bypass the executable and boundary evidence required by ADR-0014.
- **Revisit when**: A packet proves three maintained primary sources, two materially distinct executable local examples, one contradicting implementation choice, a sanitised worked exemplar, a reviewable drill and a clear boundary from analytics and data engineering.

## Pruned

### LES-0012 · Inception necessarily writes to main

- **Lesson**: Inception necessarily writes to main, because the org that mandates branches is being compiled during the writes.
- **Origin**: harvest
- **Venture**: Venture C
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
- **Venture**: Venture C
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
- **Venture**: Venture B
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
- **Venture**: Venture B
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
- **Venture**: Venture B
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
- **Venture**: Venture B
- **Source note**: Estate survey at EOS creation.
- **Evidence class**: observational
- **Disposition**: estate-default
- **Outcome**: The archived WG-DEL-003 supplied the original ruling. The live decision is `WG-ARCH-006`, which treats visual regression inside a pinned container as deterministic change proof.
- **Scope**: estate
- **Applies when**: Test suites comparing rendered screenshots across machines.
- **Informs**: packs/delivery-testing/PACK.md, WG-ARCH-006
- **Decided**: 2026-07
- **Pruned**: 2026-08-03

### LES-0022 · Migrations: forward-only, idempotent, advisory-locked

- **Lesson**: Migrations: forward-only, idempotent, advisory-locked, run before app start, fail closed.
- **Origin**: harvest
- **Venture**: Venture B
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
- **Venture**: Venture B
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
