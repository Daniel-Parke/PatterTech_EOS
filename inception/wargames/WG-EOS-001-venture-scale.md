---
summary: What scale of organisational machinery does this venture compile, S, M or L?
type: wargame
tags: [eos, wargame]
status: active
review_by: 2027-07
---

# WG-EOS-001: What scale of organisational machinery does this venture compile?

## The question

Every Session 0 compiles a seed from the kernel, and the seed's size is
the single largest ceremony decision the venture ever takes. Too small
and legal duties or coordination fail silently; too large and the
ceremony kills small work (the failure mode the EOS was built against).
The scale is ruled once at inception and re-ruled only through rescale
(PB-E08) when a trigger changes.

## It depends on

- Lifespan: a weekend artefact or a going concern?
- Server state or auth: does anything persist or log in?
- Money: does money change hands under this venture's name?
- Personal or regulated data: does the law watch this venture?
- Ops burden: does anything need deploying, monitoring, backing up?
- A second human: does anyone besides the operator hold decisions?

## Options

### S. Six operating files, no org
Routers, brief, lock-book, worklog, feedback (kernel/SCALE_MATRIX.md
is exact). One human, one log, no roles. Costs nothing to run; offers
no separation of duties and no compliance machinery.

### M. The lite org
Adds the constitution (product slot filled), collapsed tiers T1 to T3
with gates G1 to G3, the three role charters, a single queue file,
three cadences, the questions file. Separation of duties without the
work-order file system.

### L. The full shape
Per-file work orders with claims and worktrees, tiers to T4, gates to
G5, knowledge shelves, practice audits, scoreboard. The AutoWatt
shape; verification bandwidth becomes the limiting resource.

## Decision rule

All six triggers silent: S. Any of server state, auth, standing ops
or a lifespan beyond a quarter: at least M. Any of money under
contract, personal or regulated data as working material, a second
human holding decisions, or a multi-surface estate with deploys: L.
Trigger add-ons attach regardless of scale (a compliance registry the
moment regulated data appears; see the matrix). Torn between two
scales, take the smaller and write the rescale condition into the
lock-book; rescale is cheap and deliberate, over-ceremony is a
standing tax.

## Default

The smallest scale the triggers allow. Ceremony must be earned by
risk, never by ambition.

## Worked rulings

- **AutoWatt (2026-07, argued)**: L. All six triggers fire: contracted
  money, live UK data duties, auth and server state, an AWS estate, a
  second human (Gareth), multi-year lifespan. Landed in the reseed
  lock-book header.
- **PatterTech_Website (2026-07, argued)**: S. Static brochure and
  journal, no state, no money, one human; ruled retroactively at EOS
  creation, recorded in registry/PROJECTS.md. Rescale condition: any
  server-handled form or reader accounts.
