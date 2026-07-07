---
summary: What the PatterTech EOS is and how the repo is laid out
type: root
tags: [eos]
---

# PatterTech EOS

The PatterTech Engineering Operating System. A documentation-and-process
repo, no build, that seeds and governs our ventures so AI agents can
take a project from idea to operated software without re-learning the
same lessons every time.

Two halves, unified in v1.0 (see `org/decisions/ADR-0001`):

- **Knowledge**: `doctrine/` holds the argued rules, derivation methods,
  patterns and wargames per domain. `registry/` holds what is true today
  (stack profiles, trusted vendors, the venture directory, lessons).
- **Execution**: `kernel/` holds the organisational machinery (roles,
  work orders, gates, cadences, templates) that Session 0 compiles into
  each venture at the smallest scale that fits. `inception/` is the
  Session 0 system itself.

The EOS runs on its own kernel: `org/` carries its state, work queue,
cadences, playbooks, decisions and logs.

New here? `GUIDE.md` is the all-in-one field guide: it teaches the whole
system from first principles, walks the AutoWatt genesis, and shows the
development lifecycle end to end, pointing to the canonical files as it
goes. Read it once, then use the map below and `INDEX.md` for lookup.

## Map

| Path | What lives there |
| --- | --- |
| `AGENTS.md` / `CLAUDE.md` | Entry point and never-list (byte-identical) |
| `START.md` | Read order per entry mode, ground rules |
| `GUIDE.md` | The all-in-one field guide (framework, genesis, lifecycle) |
| `INDEX.md` | Derived index of every file, grep the tag column |
| `GOVERNANCE.md` | Promotion numbers, schema, tags, protected set |
| `OPERATORS_GUIDE.md` | Daniel's manual for running the EOS |
| `kernel/` | Templates compiled into ventures, scale matrix, seed rubric |
| `inception/` | Session 0: interview, scale wargame, walk order, compile |
| `doctrine/` | Knowledge modules and their wargames |
| `registry/` | Projects, vendors, lessons, stack profiles |
| `org/` | The EOS's own state, queue, cadences, playbooks, decisions |
| `examples/` | Worked instantiations |
| `tools/eos_check.py` | The check tool (`--repo`, `--seed`, `--write-index`) |

## Consuming the EOS

A venture never reads this repo at random. Session 0 compiles it a seed
pack: thin agent routers, a lock-book of rulings, distilled standards
and, where scale demands it, an org kernel. The venture pins the EOS
version it was compiled from and upgrades deliberately. Working agents
read the venture's own files first and follow citations back here.

## Related repos

- `AutoWatt`: the org kernel ancestor; its seed pack is the extraction
  source for `kernel/templates/`.
- `PatterTech_Website`: the first conforming web project and the worked
  example in `examples/pattertech-website.md`.
- `WiseWattage`, `PatterTech_Business`: extraction sources for the
  architecture, delivery and devops modules.
