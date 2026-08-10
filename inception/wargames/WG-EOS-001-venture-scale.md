---
summary: What scale of organisational machinery does this venture compile, S or ORG?
kind: guide
scope: eos-internal
authority: default
lifecycle: active
basis: local-observation
evidence_grade: observational
volatility: slow
review: 2027-07
type: wargame
tags: [eos, wargame]
status: active
---

# WG-EOS-001: What scale of organisational machinery does this venture compile?

## The question

Every Session 0 compiles a seed from the kernel, and the seed's size is
the single largest ceremony decision the venture ever takes. Too small
and legal duties or coordination fail silently; too large and the
ceremony kills small work (the failure mode the EOS was built against).
The scale is ruled once at inception and re-ruled only through rescale
when a trigger changes.

## It depends on

- Lifespan: a weekend artefact or a going concern?
- Server state or auth: does anything persist or log in?
- Money: does money change hands under this venture's name?
- Personal or regulated data: does the law watch this venture?
- Ops burden: does anything need deploying, monitoring, backing up?
- A second human: does anyone besides the operator hold decisions?

## Options

### S. Nine files, no org
Routers, operators guide, brief, lock-book, feedback, compile report,
policy and task list (kernel/SCALE_MATRIX.md is exact). One human, one
task surface, no charters, no integrator tooling. Costs nothing to
run; offers no separation of duties and no compliance machinery.

### ORG. The full shape
Adds the constitution, the boot file, the testing law, the artefact
shapes, the questions file, the playbooks, the three situational
charters (EXECUTOR, ORACLE, REVIEWER), the cadence file and the claims
file. Work becomes task records with derived views; separation of
duties exists where the router asks for it. Verification bandwidth
becomes the limiting resource.

## The v2 narrowing

v1 offered S, M and L. ADR-0002 merges M and L into a single ORG scale,
so the fork is now two-way and an existing M or L venture reads as ORG
at its next recompile. The trigger set and the decision rule below are
unchanged; only the destination of the heavier answers moved.

## Decision rule

All six triggers silent: S. Any of server state, auth, standing ops,
money under contract, personal or regulated data as working material,
a second human holding decisions, or a multi-surface estate with
deploys: ORG. Lifespan never forces a scale by itself: a long-lived
venture with no other trigger stays S with its rescale conditions
written in; what lifespan does is make the rescale conditions
mandatory, because a venture that lives will eventually trip one.
Trigger add-ons attach regardless of scale (a compliance file the
moment regulated data appears; see the matrix). Torn between the two,
take S and write the rescale condition into the lock-book; rescale is
cheap and deliberate, over-ceremony is a standing tax.

## Default

The smallest scale the triggers allow. Ceremony must be earned by
risk, never by ambition.

## Worked rulings

- **Venture A (2026-07, argued)**: L. All six triggers fire: contracted
  money, live UK data duties, auth and server state, an AWS estate, a
  second human (Gareth), multi-year lifespan. Landed in the reseed
  lock-book header, and reads as ORG at its v2 recompile.
- **PatterTech_Website (2026-07, argued)**: S. Static brochure and
  journal, no state, no money, one human; ruled retroactively at EOS
  creation, recorded in registry/PROJECTS.md. Rescale condition: any
  server-handled form or reader accounts.
- **Guth (2026-07, argued)**: M. Standing ops fires because the LAN rig
  deploys from the tree; personal data stays silent because the only
  recordings are the operator's own. Reads as ORG at its v2 recompile
  with no change of argument.
