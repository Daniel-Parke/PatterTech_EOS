---
summary: The exact seed file list per scale S, M and L, plus trigger add-ons, machine-checked
type: kernel
tags: [eos]
---

# SCALE_MATRIX

The law of what a compiled seed contains. `eos_check.py --seed` parses
the tables below and fails a seed that misses a required file. This
matrix supersedes the rough counts in ADR-0001 section 8.

Reading the numbers honestly: S is eight files, of which CLAUDE.md is a
byte copy and the compile report is meta, so the operating surface is
six. M runs about eighteen, L about twenty plus the empty directories
Genesis fills.

The scale is ruled at Session 0 by WG-EOS-001 and recorded in the
lock-book header. Rescale (PB-E08) recompiles the delta between the old
and new columns.

## The matrix

An `x` means the file is required at that scale. Every compiled file
traces to its template through the compile report; CLAUDE.md traces to
AGENTS.md as a byte copy.

| path | template | S | M | L |
| --- | --- | --- | --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md | x | x | x |
| CLAUDE.md | byte copy of AGENTS.md | x | x | x |
| OPERATORS_GUIDE.md | kernel/templates/OPERATORS_GUIDE.tpl.md | x | x | x |
| docs/VENTURE_BRIEF.md | kernel/templates/VENTURE_BRIEF.tpl.md | x | x | x |
| docs/LOCKBOOK.md | kernel/templates/LOCKBOOK.tpl.md | x | x | x |
| docs/EOS_FEEDBACK.md | kernel/templates/EOS_FEEDBACK.tpl.md | x | x | x |
| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | x | x | x |
| docs/WORKLOG.md | kernel/templates/WORKLOG.tpl.md | x | | |
| org/CONSTITUTION.md | kernel/templates/org/CONSTITUTION.tpl.md | | x | x |
| org/START.md | kernel/templates/org/START.tpl.md | | x | x |
| org/OPERATING_MODEL.md | kernel/templates/org/OPERATING_MODEL.tpl.md | | x | x |
| org/STATE.md | kernel/templates/org/STATE.tpl.md | | x | x |
| org/TEMPLATES.md | kernel/templates/org/TEMPLATES.tpl.md | | x | x |
| org/CADENCE.md | kernel/templates/org/CADENCE.tpl.md | | x | x |
| org/QUESTIONS.md | kernel/templates/org/QUESTIONS.tpl.md | | x | x |
| org/QUEUE.md | kernel/templates/org/QUEUE.tpl.md | | x | |
| org/roles/PLAN.md | kernel/templates/org/roles/PLAN.tpl.md | | x | x |
| org/roles/WORK.md | kernel/templates/org/roles/WORK.tpl.md | | x | x |
| org/roles/VERIFY.md | kernel/templates/org/roles/VERIFY.tpl.md | | x | x |
| org/playbooks/CATALOGUE.md | kernel/templates/playbooks/CATALOGUE.tpl.md | | | x |
| org/work/NEXT.md | kernel/templates/org/work/NEXT.tpl.md | | | x |

## Directories created empty

M: `org/decisions/`, `org/logs/`. L adds: `org/work/items/`,
`org/work/suggestions/`, `org/work/archive/`, `org/knowledge/registry/`,
`org/knowledge/research/`, `org/knowledge/guidance/`, `org/standards/`,
`org/practices/`, `org/product/specs/`, `org/product/updates/`,
`org/metrics/audits/`. Their contents are Genesis and delivery-loop
outputs, never seed files: the practices charter, standards, the
scoreboard and the product design set are authored by PB-001 inside the
venture, not compiled from the kernel.

## Trigger add-ons

Attached by trigger regardless of scale, named in the lock-book header
`addons:` list. The seed check enforces the files of every named
add-on. An add-on without a kernel template is authored at Session 0
from the doctrine the trigger names and recorded in the compile report
as `authored`.

| addon | file | source | note |
| --- | --- | --- | --- |
| compliance | org/knowledge/registry/REG-COMP-<JURIS>-001.md | authored per the registry row pattern | personal or regulated data present; at S, rescale to M first |
| ops-runbook | ops/runbooks/deploy.md | authored per the stack profile | anything deployed with server state |
| restore-test | org/CADENCE.md gains the restore-test row | kernel/templates/org/CADENCE.tpl.md | production data exists |

Notes:

- The queue file swaps for the work-order system between M and L
  (org/QUEUE.md against org/work/NEXT.md plus per-file orders); a
  rescale migrates open items across.
- docs/WORKLOG.md exists only at S; M and L log per session under
  `org/logs/`.
- The lock-book lives at `docs/LOCKBOOK.md` at every scale, so tooling
  and humans always know where the rulings are.
