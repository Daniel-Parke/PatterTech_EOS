---
summary: Ancestry proof for the current-HEAD S seed fixture
type: template
tags: [eos]
compiled_from: kernel/templates/COMPILE_REPORT.tpl.md
---

# Compile report

## Ancestry

| file | source |
| --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md |
| CLAUDE.md | byte copy of AGENTS.md |
| OPERATORS_GUIDE.md | kernel/templates/OPERATORS_GUIDE.tpl.md |
| docs/VENTURE_BRIEF.md | kernel/templates/VENTURE_BRIEF.tpl.md |
| docs/LOCKBOOK.md | kernel/templates/LOCKBOOK.tpl.md |
| docs/RULINGS.json | kernel/templates/RULINGS.tpl.json |
| docs/EOS_FEEDBACK.md | kernel/templates/EOS_FEEDBACK.tpl.md |
| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md |
| docs/PRODUCT_MAP.md | kernel/templates/PRODUCT_MAP.tpl.md |
| docs/ACCEPTANCE_SPINE.md | kernel/templates/ACCEPTANCE_SPINE.tpl.md |
| docs/genesis/WORK_PACKAGE.md | kernel/templates/WORK_PACKAGE.tpl.md |
| docs/genesis/RESEARCH_PACKET.md | kernel/templates/RESEARCH_PACKET.tpl.md |
| docs/genesis/LENS.md | kernel/templates/LENS.tpl.md |
| docs/policy.json | kernel/templates/org/policy.tpl.json |
| docs/TASKS.md | kernel/templates/TASKS.tpl.md |

## Check result

This committed fixture is accepted only when
`python -m tools.eos check --seed examples/current-head-seed` is clean.
