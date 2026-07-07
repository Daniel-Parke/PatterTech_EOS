---
summary: One entry per release tag, sectioned by area
type: governance
tags: [eos]
---

# CHANGELOG

Newest first. One entry per release tag; the Unreleased section
accumulates until the next tag. Sections: kernel, doctrine, inception,
registry, org, tools.

## Unreleased (building towards v1.0.0)

- **org**: ADR-0001 accepted, the v1.0 architecture. The EOS now runs on
  its own lite kernel (state, queue, cadences, playbooks, logs).
- **doctrine**: modules/ became doctrine/. Wargames renamed to
  module-prefixed IDs (WG-WEB-001 to 014). Cost and hardware stubs
  retired to roadmap rows. MODULE_SHAPE.md added. v4 web-design
  learnings captured (heading sweep, live rule, WG-WEB-013, WG-WEB-014).
  C2 populated the voice module: the seven-rule voice law with
  examples, the banned-list pattern, and WG-VOX-001 (audience register,
  default professional-calm), walked in every Session 0.
- **kernel**: created with the compile contract; LOCKBOOK.tpl.md
  migrated from the v0.1 project lock-in, full templates due in Phase B.
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
  alarm).
- **registry**: created; projects, vendors, lessons and the static web
  stack profile seeded. D1 updated the AutoWatt row: reseed compiled to
  a green seed check on branch reseed/eos-v1, awaiting the rubric
  signature.
- **tools**: eos_check.py added (checks E001 to E010, --repo and --seed
  modes, index generation).
- **roots**: AGENTS.md canonical with CLAUDE.md byte parity, START.md
  entry modes, GOVERNANCE.md, OPERATORS_GUIDE.md, evolved VISION.md.
