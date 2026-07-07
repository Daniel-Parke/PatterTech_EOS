---
summary: The compile contract, scale system and concurrency doctrine for the kernel
type: kernel
tags: [eos]
---

# Kernel

The organisational machinery that Session 0 compiles into each venture.
Nothing in here is read by a venture at runtime; ventures get compiled
copies, stamped with the EOS version they came from.

Status: Phase B in flight. The org templates (constitution, start, the
three role charters) landed with B1; the rest arrive through B4, all
extracted from the Venture A seed pack at commit d2e3250.
`templates/LOCKBOOK.tpl.md` is the migrated v0.1 lock-in awaiting its
Phase B rebuild.

## The compile contract

- Templates are hand-written. The compiler (an agent following
  `inception/COMPILE.md`) is a slot-filler and pruner, never an author.
- Slots look like `{{PRODUCT_DOCTRINE}}` and are filled from the venture
  brief and lock-book. A compiled file with an unfilled slot fails the
  seed check (E008).
- Scale markers look like `<!-- scale: M L -->` and fence sections that
  only exist at those scales. A fence closes with `<!-- scale: end -->`,
  and markers wrap whole sentences, bullets or sections, never fragments
  of a sentence. The compiler keeps a fenced body only when the
  venture's scale is listed and always removes the marker lines; a
  leftover marker of either kind fails the seed check.
- Every compiled file's template ancestry is listed in the venture's
  compile report. A seed file that cannot be traced to a template plus
  rulings is a compile failure.
- `kernel/SCALE_MATRIX.md` (Phase B) names the exact file list per scale
  S, M and L, plus trigger-attached add-ons. `kernel/SEED_RUBRIC.md`
  (Phase B) is the pass gate, items split auto versus human.

## Concurrency doctrine

Isolation comes from git worktrees, path-glob claims on work orders and
WIP limits. Never from lock files in a shared tree: they are racy, they
go stale after crashed sessions, and the estate's own job queue already
learned to pair every advisory lock with a stale-claim reaper. The one
soft claim in the system is the `active_session` line in a STATE file,
checked at session start and swept for staleness.

## The harness mapping

Published long-running-agent harnesses converge on organs this kernel
already has. So nobody bolts a parallel system on top: a granular
pass/fail feature list is the work order's acceptance boxes; the
progress file is STATE.md with its Resume Packet; one feature per
session is one work order per session; verify-the-environment-first is
the WORK charter's opening step; leave-it-production-ready is the
close-out ritual and the releasable-main article.
