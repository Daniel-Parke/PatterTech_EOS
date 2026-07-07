---
summary: The ordered build queue for the EOS, phases B to F and the release
type: org
tags: [eos]
---

# QUEUE

The EOS's work queue, ordered. A build session (entry mode 2) takes the
top unblocked item, follows its playbook, and closes out. One item per
session unless items are trivially small. WIP is 1. Items B1 to D2 are
the critical path: AutoWatt's reseed and Genesis wait on them.

## Ready

### F2. Delivery module
- phase: F · playbook: PB-E03 · claims: `doctrine/delivery/`
- Test-first-where-the-type-demands, ratchets, coverage floors, VRT
  pinning, gate rubrics (fixing the v0.1 gap), WG-DEL wargames (coverage
  level, e2e weighting, VRT scope, flake policy).
- done when: as F1.

### F3. Devops module
- phase: F · playbook: PB-E03 · claims: `doctrine/devops/`
- Migrations doctrine, environments, secrets, restore-test regime,
  WG-OPS wargames (hosting, containers, backups, cost ceilings).
- done when: as F1.

### E3. S-scale ergonomics (drill findings, S-0011)
- phase: E follow-up · playbook: PB-E03 · claims: `kernel/templates/`
- A sanctioned deferral convention for the lock-book's design slots at
  S (or S fences for the token and QC sections), a blessed home for
  operator questions at S (the worklog's questions section formalised
  in WORKLOG.tpl.md, provenance-honest), and consider mandating the
  drill agent's queue ordering: operator-independent work first.
- done when: templates amended, eos_check --repo green, drill findings
  6 and 8 closed.

### E4. Web defaults that presuppose the house brand (drill findings, S-0011)
- phase: E follow-up · playbook: PB-E03 · claims:
  `doctrine/web-design/wargames/`
- Sharpen decision rules (not defaults) of WG-WEB-004, 009, 010, 011 so
  non-house brands stop arguing around house assumptions: name the
  brand-physics trigger in each rule. Defaults move only via PB-E04
  promotion numbers; the drill's rulings are synthetic and count
  nothing.
- done when: four decision rules name their triggers, budgets hold,
  indexes fresh.

### REL. Release v1.0.0
- phase: release · playbook: PB-E05 · claims: repo-wide
- CHANGELOG entry, tag v1.0.0. Then Daniel's manual step: folder rename,
  the two PatterTech_Website reference updates, private GitHub remote,
  push with tags (OPERATORS_GUIDE troubleshooting section has the
  commands).
- done when: tag pushed, PROJECTS rows note the new home.

## Blocked

### D1. AutoWatt reseed: awaiting Daniel's rubric signature
- phase: D · playbook: PB-E01 (compile phases only) · session S-0008
- Everything mechanical is done: seed compiled on AutoWatt branch
  reseed/eos-v1 (commit e7d0a8f), eos_check --seed green 0/0,
  seventeen rulings (nine argued), compile report written, two feedback
  entries banked. Blocked solely on the human rubric items H1 to H5 in
  the AutoWatt docs/COMPILE_REPORT.md.
- done when: Daniel signs, merges the branch, PROJECTS pin moves to the
  merged commit. Genesis is then unblocked.

## Done

- A. Phase A: migration, roots, governance, registries, org instance,
  check tool (session S-0001, 2026-07-07).
- B1. Kernel extraction: constitution, start, roles (session S-0002,
  2026-07-07).
- B2. Kernel extraction: operating model, templates, state, cadence,
  questions (session S-0003, 2026-07-07).
- B3. Kernel extraction: playbooks, operators guide, agent routers
  (session S-0004, 2026-07-07).
- B4. Scale matrix, seed rubric, venture templates, seed checks
  (session S-0005, 2026-07-07).
- C1. Compile rules and walk order (session S-0006, 2026-07-07).
- C2. Voice module (session S-0007, 2026-07-07).
- D2. Worked example and reseed harvest (session S-0009, 2026-07-07).
- E1. Inception system (session S-0010, 2026-07-07).
- E2. S-scale drill: pass, eight findings, three fixed in session, two
  queued as E3 and E4 (session S-0011, 2026-07-07).
- R1. Stack profiles from the estate (session S-0012, 2026-07-07).
- F1. Architecture module (session S-0013, 2026-07-07).
