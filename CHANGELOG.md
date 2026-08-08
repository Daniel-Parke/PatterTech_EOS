---
summary: One entry per release tag, sectioned by area
type: governance
tags: [eos]
---

# CHANGELOG

Newest first. One entry per release tag; the Unreleased section
accumulates until the next tag. Sections: kernel, doctrine, inception,
registry, org, tools.

## Unreleased (towards v2.0.0, not released)

The v2 overhaul, built under ADR-0002 and corrected under ADR-0003.
Held at the release checkpoint. The first gate run reported three of
six numeric gates missed; the 2026-08-04 pre-release review then found
that no code computes any gate figure, that one gate's verdict turns on
an unwritten convention for an undefined ratio, and that the freeze
manifest fails its own hash check. The benchmark is being rebuilt and
re-run before any gate is reported again. See
org/reports/V2_FINAL_REPORT.md, "Corrections, 2026-08-04".

- **kernel**: ten-article constitution; EXECUTOR, ORACLE and REVIEWER
  replace the PLAN, WORK and VERIFY trinity; policy and cadence become
  JSON; the scale matrix moves to S and ORG, with a seed resolving
  whichever matrix its pinned commit carries. Ten v1 templates retired
  with every load-bearing rule's destination recorded.
- **packs**: doctrine becomes twenty progressive-disclosure packs across
  the estate's domains, each meeting an eleven-point definition of done.
  The house visual language becomes an opt-in preference pack, so a
  venture can choose another design philosophy without deviation
  machinery. WG-DEL-005 is written at last, with 006 and 007 beside it.
- **governance**: graded evidence path (experiment, ADR) replaces
  wargame-first; precedence scopes venture rulings locally and protects
  law and standard based rules from vote counts; the protected set
  shrinks to seven items with security-privacy as canonical home for
  four of them.
- **tools**: one 445-line script becomes a tested package behind
  python -m tools.eos, with structural, semantic, seed and freshness
  checks, the deterministic router, the fail-closed guard, context
  packets, task and claim operations, migration and benchmark commands.
  338 tests on Python 3.11 and 3.14. The v1 checker is a forwarding shim.
- **benchmark**: a frozen suite of eleven tasks and three probes, 155
  scored runs in the ledger across v1, v2, v2-routed-once, the routing
  ablation and the timing ablation, an evidence ledger of 448
  individually recorded sources, and a sealed final suite awaiting the
  operator's key. The 84 first quoted here counted only the v1 baseline
  and the superseded v2 arm, and excluded the 45 runs the gate table is
  actually computed from.
- **governance**: ADR-0003 rules that retained material which misleads an
  agent is a defect, that the archive of record is a pushed tag rather
  than a directory, and that a file marked derived must have a live
  generator. packs/INDEX.md had listed eight of twenty packs, so twelve
  packs were unreachable through the sanctioned activation path;
  packs/GUIDE_INDEX.md had omitted 79 of 86 guides. Both now generate,
  scoped to live material. registry/coverage.json's twelve stale Wave B
  rows are repaired and S013 validates the matrix against its schema and
  against the packs on disk.
- **inception**: Session 0 becomes a pack activation walk with a risk
  surface map, plus an Express path for reversible S ventures.
- **org**: the EOS runs on its own v2 machinery: policy, task records,
  committed claims, generated views. v1 org files archived verbatim.

## Superseded, towards v1.1.0 (never released)

- **roots**: GUIDE.md added, the all-in-one field guide. A teaching
  layer over the whole system (framework, the AutoWatt genesis, the
  development lifecycle) that cross-links to the canonical files rather
  than duplicating them, so it stays honest under the one-writer-per-fact
  rule. Session S-0020. Additive; the pointer lives in README.md.

## v1.0.0 · 2026-07-07

The founding release: the full kernel, the inception system proven by
a cold drill, five doctrine modules, the estate registries and the
check tool, built across sessions S-0001 to S-0018 per ADR-0001. The
folder rename to PatterTech_EOS, the private remote and the tag push
are the operator's manual close (OPERATORS_GUIDE troubleshooting has
the commands).

- **org**: ADR-0001 accepted, the v1.0 architecture. The EOS now runs on
  its own lite kernel (state, queue, cadences, playbooks, logs).
- **doctrine**: modules/ became doctrine/. Wargames renamed to
  module-prefixed IDs (WG-WEB-001 to 014). Cost and hardware stubs
  retired to roadmap rows. MODULE_SHAPE.md added. v4 web-design
  learnings captured (heading sweep, live rule, WG-WEB-013, WG-WEB-014).
  C2 populated the voice module: the seven-rule voice law with
  examples, the banned-list pattern, and WG-VOX-001 (audience register,
  default professional-calm), walked in every Session 0. F1 populated
  the architecture module: seven binding rules, eight WG-ARCH wargames
  argued from the estate's ADRs (boundary enforcement, ORM or raw SQL,
  derived state, job execution, the contract seam, proof of harmless
  change, vendor seams, database topology) and the ADR template. F2
  populated the delivery module: six rules including gate-is-a-rubric,
  and WG-DEL-001 to 004 (coverage ratchets, e2e weighting, VRT scope,
  flake policy). F3 populated the devops module: six rules (migrations,
  local parity, secrets, no console-clicking, proven restores, cost as
  design input) and WG-OPS-001 to 004 (hosting, containers, backups and
  restore, cost ceilings).
- **kernel**: created with the compile contract; LOCKBOOK.tpl.md
  migrated from the v0.1 project lock-in, full templates due in Phase B.
  D2's harvest amended two templates from reseed feedback: the
  constitution footer's AMENDMENT_HISTORY slot and the compile report's
  normalised and preserved ancestry row kinds.
  B1 landed the org templates from AutoWatt@d2e3250: the constitution
  (product-doctrine slot, Parts II and III renumbered per part), START
  and the three role charters, the three-strikes rule woven through,
  scale fences specified with a closing marker in kernel/README.md.
  B2 added the operating model (tiers and gates collapse at M scale),
  the canonical artefact formats including the M queue-row shape, STATE
  with the claim protocol and Resume Packet spec, the cadence schedule
  (founder update generalised to stakeholder update) and the questions
  queue. B3 added the venture router (compiled cap 40 lines, S points
  at the lock-book and worklog, M and L at the org), the operators
  guide with per-scale launcher libraries, and the playbook catalogue
  PB-001 to PB-051. B4 closed the phase: SCALE_MATRIX (S eight files, M
  eighteen, L nineteen plus empty dirs, trigger add-ons), SEED_RUBRIC
  (auto items A1 to A10 keyed to check IDs, human items H1 to H5 headed
  by the cold-start test), the lock-book rebuilt with the machine
  rulings header, and the venture brief, feedback, compile report,
  worklog, queue and NEXT templates.
- **inception**: shape fixed, system due in phases C and E. C1 landed
  COMPILE.md (prune, fill, distil, report, and the compiler's
  never-list) and WALK_ORDER.md (trigger-filtered walk, canonical
  module order, the draft-wargame escape, the twenty-ruling budget
  alarm). E1 completed the system: INCEPTION.md (phases A to E),
  INTERVIEW.md (twelve questions, three challenge steps), WG-EOS-001
  (venture scale, six triggers, argued rulings from AutoWatt and the
  website) and WG-EOS-002 (repo shape, default monorepo, estate
  rulings). E2 ran the S-scale drill cold and passed it: seed check
  green first run, the cold-start test passed live, and the findings
  fixed the lifespan clause, the spend and concrete-facts interview
  gaps and the walk budget, with S ergonomics and four house-brand
  default assumptions queued as E3 and E4. The canned brief lives at
  inception/briefs/BRIEF-S-brochure.md.
- **registry**: created; projects, vendors, lessons and the static web
  stack profile seeded. D1 updated the AutoWatt row: reseed compiled to
  a green seed check on branch reseed/eos-v1, awaiting the rubric
  signature.
- **tools**: eos_check.py added (checks E001 to E010, --repo and --seed
  modes, index generation).
- **roots**: AGENTS.md canonical with CLAUDE.md byte parity, START.md
  entry modes, GOVERNANCE.md, OPERATORS_GUIDE.md, evolved VISION.md.
