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
- **kernel**: created with the compile contract; LOCKBOOK.tpl.md
  migrated from the v0.1 project lock-in, full templates due in Phase B.
  B1 landed the org templates from AutoWatt@d2e3250: the constitution
  (product-doctrine slot, Parts II and III renumbered per part), START
  and the three role charters, the three-strikes rule woven through,
  scale fences specified with a closing marker in kernel/README.md.
- **inception**: shape fixed, system due in phases C and E.
- **registry**: created; projects, vendors, lessons and the static web
  stack profile seeded.
- **tools**: eos_check.py added (checks E001 to E010, --repo and --seed
  modes, index generation).
- **roots**: AGENTS.md canonical with CLAUDE.md byte parity, START.md
  entry modes, GOVERNANCE.md, OPERATORS_GUIDE.md, evolved VISION.md.
