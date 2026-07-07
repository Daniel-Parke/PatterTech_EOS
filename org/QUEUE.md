---
summary: The ordered build queue for the EOS, phases B to F and the release
type: org
tags: [eos]
---

# QUEUE

The EOS's work queue, ordered. A build session (entry mode 2) takes the
top unblocked item, follows its playbook, and closes out. One item per
session unless items are trivially small. WIP is 1. The v1.0 build is
complete bar REL; AutoWatt's Genesis waits only on the D1 signature.

## Ready


## Blocked

### REL. Release v1.0.0: awaiting Daniel's manual close
- phase: release · playbook: PB-E05 · session S-0018
- Checks green, CHANGELOG v1.0.0 entry written, tag v1.0.0 created
  locally. Blocked on the manual close: folder rename to
  PatterTech_EOS, the two PatterTech_Website reference updates, the
  private GitHub remote, push with tags, PROJECTS rows updated with
  the new home (commands in OPERATORS_GUIDE troubleshooting).
- done when: tag pushed, PROJECTS rows note the new home.

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
- F2. Delivery module (session S-0014, 2026-07-07).
- F3. Devops module (session S-0015, 2026-07-07).
- E3. S-scale ergonomics from the drill (session S-0016, 2026-07-07).
- E4. Web decision rules sharpened for non-house brands (session
  S-0017, 2026-07-07).
