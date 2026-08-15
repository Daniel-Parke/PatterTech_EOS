---
summary: FieldKit lock-book, the M-scale rulings and contracts with the EOS
type: template
tags: [eos]
compiled_from: kernel/templates/LOCKBOOK.tpl.md
eos_root: PatterTech_EOS
eos_version: 1.0.0
eos_commit: ba34d01
scale: M
stack: STACK-fastapi-postgres
addons: []
compiled: 2026-08-02
rulings:
  - WG-EOS-001 · M · argued · server state and auth fire; no money; login email the only pii
  - WG-WEB-007 · server · argued · survey records need a database and sign-in
  - WG-ARCH-002 · raw SQL · inherited · stack profile default taken
  - WG-OPS-001 · managed host · inherited · default taken
  - WG-OPS-003 · nightly backups · inherited · restore-test add-on attaches at first production data
  - WG-DEL-001 · standard coverage · inherited · profile default taken
---

# FieldKit lock-book

The venture's contract with the EOS. This file wins on specifics; EOS
doctrine wins on principles. The YAML header above is machine-read: the
seed check validates it, the harvest counts its rulings, upgrades diff
against its pins. Rulings rows are one line each,
`WG-ID · ruling · argued|inherited · note`; argued means the triggers
were engaged afresh, inherited means the default was taken without new
argument. Only argued rulings are promotion evidence.

Note on `addons: []`: nothing is deployed at Session 0, so no add-on
trigger has fired yet. The ops-runbook add-on attaches at the first
deploy and the restore-test add-on at the first production data, per
the trigger table in the scale matrix; both are noted here and in the
brief so neither is forgotten.

## Identity

- One-word feel: dependable
- Signature motif (promoted everywhere): set at first build; ruled at
  the first-build lock-in via org/QUEUE.md
- Signature animated pieces (the sanctioned exceptions, by name): set
  at first build; ruled at the first-build lock-in via org/QUEUE.md
- Voice register ruling (WG-VOX-001): in the header; banned list per
  the voice module.

## Narrative brief

The one-paragraph story the design must tell without saying it: what
the visitor should feel, what stays concealed, what escapes anyway.
Name the physics or motifs the brand draws from and how each becomes a
mechanism, not a mood board. This paragraph drives the light budget
(WG-WEB-005), the reactivity ruling (WG-WEB-011) and the imagery ruling
(WG-WEB-012).

A surveyor on a windy site with one bar of signal should feel the app
is quicker than paper, and the office should feel the record is the
firm's own: complete, current and exportable. Nothing decorative
stands between a field worker and a saved survey; the design's whole
argument is speed, legibility on a phone in daylight, and the quiet
confidence of a record that does not get lost.

## Tokens

Before a first build exists, design-system slots below take the
sanctioned deferral: `set at first build` plus where the value gets
ruled. The first-build lock-in session replaces every deferral in one
sitting and notes it in the worklog or queue.

- Token home: set at first build; ruled at the first-build lock-in via
  org/QUEUE.md · Code mirror: set at first build; ruled at the
  first-build lock-in via org/QUEUE.md · Styleguide route: set at
  first build; ruled at the first-build lock-in via org/QUEUE.md
- Surface ladder: set at first build; ruled at the first-build lock-in
  via org/QUEUE.md
- Accents: set at first build; ruled at the first-build lock-in via
  org/QUEUE.md
- Text tiers and measured contrast: set at first build; ruled at the
  first-build lock-in via org/QUEUE.md
- Measures: reading set at first build · wide set at first build ·
  full set at first build · block gap set at first build; all ruled at
  the first-build lock-in via org/QUEUE.md

## QC gates (exact commands)

- Build: set at first build; ruled at the first-build lock-in via
  org/QUEUE.md
- Overflow at 375: set at first build; ruled at the first-build
  lock-in via org/QUEUE.md
- Page weight: set at first build; ruled at the first-build lock-in
  via org/QUEUE.md
- Screenshots: set at first build; ruled at the first-build lock-in
  via org/QUEUE.md
- Regression smokes: set at first build; ruled at the first-build
  lock-in via org/QUEUE.md

## Structural contracts (things future edits must not break)

- Survey records are append-only; a correction is a new version, never
  an edit in place.
- The login email is the only personal data stored, and it never lands
  in logs.
- Exports leave clean as CSV, so the firm's data is never captive.

## Deviations from doctrine

None, or one entry each: the doctrine deviated from, the trigger that
justifies it, the wargame that argued it (a draft wargame in
docs/EOS_FEEDBACK.md if none exists), and the operator's approval.
Deviations are harvested as contrary rulings.

None.
