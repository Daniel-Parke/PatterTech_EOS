---
summary: The ordered build queue for the EOS, phases B to F and the release
type: org
tags: [eos]
---

# QUEUE

The EOS's work queue, ordered. A build session (entry mode 2) takes the
top unblocked item, follows its playbook, and closes out. One item per
session unless items are trivially small. WIP is 1. Items B1 to D2 are
the critical path: Venture A's reseed and Genesis wait on them.

## Ready

### E2. S-scale drill
- phase: E · playbook: PB-E07 · claims: none (scratch venture repo)
- Canned brief: a static brochure site. A cold session runs Session 0
  end to end. Grade the seed, file findings as queue items.
- done when: drill report written, findings queued.

### R1. Stack profiles from the estate
- phase: F · playbook: PB-E03 · claims: `registry/stacks/`
- STACK-fastapi-postgres.md and STACK-fullstack-app.md from WiseWattage
  (include the urllib3 cap and Docker-on-Windows lessons).
- done when: profiles cited by stacks README, review_by set.

### F1. Architecture module
- phase: F · playbook: PB-E03 · claims: `doctrine/architecture/`
- Doctrine (rings, boundaries as records, ADR practice, deterministic
  builds, contract drift) plus six to ten WG-ARCH wargames extracted
  from WiseWattage, PatterTech_Business, Venture A ADRs. ADR template.
- done when: MODULE_SHAPE holds, wargames indexed, budgets hold.

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
