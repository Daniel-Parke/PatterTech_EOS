---
summary: The ordered build queue for the EOS, phases B to F and the release
type: org
tags: [eos]
---

# QUEUE

The EOS's work queue, ordered. A build session (entry mode 2) takes the
top unblocked item, follows its playbook, and closes out. One item per
session unless items are trivially small. WIP is 1. The v1.0 build is
complete bar REL; Venture A's Genesis waits only on the D1 signature.

## Ready

### REL. Release v1.0.0
- phase: release · playbook: PB-E05 · claims: repo-wide
- CHANGELOG entry, tag v1.0.0. Then Daniel's manual step: folder rename,
  the two PatterTech_Website reference updates, private GitHub remote,
  push with tags (OPERATORS_GUIDE troubleshooting section has the
  commands).
- done when: tag pushed, PROJECTS rows note the new home.

## Blocked

### D1. Venture A reseed: awaiting Daniel's rubric signature
- phase: D · playbook: PB-E01 (compile phases only) · session S-0008
- Everything mechanical is done: seed compiled on Venture A branch
  reseed/eos-v1 (commit e7d0a8f), eos_check --seed green 0/0,
  seventeen rulings (nine argued), compile report written, two feedback
  entries banked. Blocked solely on the human rubric items H1 to H5 in
  the Venture A docs/COMPILE_REPORT.md.
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
