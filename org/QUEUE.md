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

### B1. Kernel extraction: constitution, start, roles
- phase: B · playbook: PB-E03 · claims: `kernel/templates/org/`
- From AutoWatt@d2e3250: CONSTITUTION.tpl.md (Part I becomes the
  `{{PRODUCT_DOCTRINE}}` slot; Parts II and III generic, protected),
  START.tpl.md, roles/PLAN|WORK|VERIFY.tpl.md. Add the three-strikes
  rule to the operating rules and all three charters. Scale markers on
  everything M-and-up.
- done when: files carry `template: true` and `extracted_from`, slots
  and markers follow kernel/README.md, eos_check --repo green.

### B2. Kernel extraction: operating model, templates, state, cadence, questions
- phase: B · playbook: PB-E03 · claims: `kernel/templates/org/`
- OPERATING_MODEL.tpl.md (tiers and gates collapse at M scale via
  markers), TEMPLATES.tpl.md (front-matter contracts), STATE.tpl.md
  (Resume Packet spec plus active_session line), CADENCE.tpl.md,
  QUESTIONS.tpl.md.
- done when: as B1.

### B3. Kernel extraction: playbooks, operators guide, agent routers
- phase: B · playbook: PB-E03 · claims: `kernel/templates/`
- playbooks/CATALOGUE.tpl.md (PB-001 to PB-051; founder update becomes
  stakeholder update), OPERATORS_GUIDE.tpl.md (launchers with scale
  markers), AGENTS.tpl.md (venture router, hard cap 40 lines).
- done when: as B1.

### B4. Scale matrix, seed rubric, venture templates, seed checks
- phase: B · playbook: PB-E03 · claims: `kernel/`, `tools/`
- SCALE_MATRIX.md (exact file list per S, M, L plus trigger add-ons),
  SEED_RUBRIC.md (auto items keyed to check IDs, human items with the
  cold-start test first), rebuild LOCKBOOK.tpl.md with the YAML rulings
  header, VENTURE_BRIEF.tpl.md, EOS_FEEDBACK.tpl.md,
  COMPILE_REPORT.tpl.md. Turn on eos_check --seed against the matrix.
- done when: `eos_check.py --seed` validates a hand-made fixture seed.

### C1. Compile rules and walk order
- phase: C · playbook: PB-E03 · claims: `inception/`
- COMPILE.md (prune, fill, distil, report) and WALK_ORDER.md (filter
  WARGAME_INDEX by triggered domains, canonical ordering).
- done when: a dry run on paper against the fixture seed reads clean.

### C2. Voice module
- phase: C · playbook: PB-E03 · claims: `doctrine/voice/`
- DOCTRINE.md (the voice law with examples), the banned-list pattern,
  WG-VOX-001 audience register. Compiled into every seed at every scale.
- done when: module passes MODULE_SHAPE, indexed, budgets hold.

### D1. AutoWatt reseed (time-critical, doubles as the L-scale drill)
- phase: D · playbook: PB-E01 (compile phases only) · claims: none here
  (writes happen in the AutoWatt repo)
- Compile AutoWatt's new seed from kernel templates. Its existing brief,
  product doctrine, UK registry, ADRs and logs slot straight in; they
  are the kernel's ancestors. Walk web-design and voice wargames for its
  website surfaces into a lock-book with argued rulings. Add
  EOS_FEEDBACK.md. Write the compile report. Grade against SEED_RUBRIC.
- done when: eos_check --seed green on the AutoWatt repo, Daniel signs
  the human rubric items, PROJECTS.md row updated with the new pin.
  AutoWatt Genesis is then unblocked.

### D2. Worked example and reseed harvest
- phase: D · playbook: PB-E02 · claims: `examples/`, `registry/`
- Write examples/autowatt-seed.md from the reseed. Harvest lessons from
  the compile into LESSONS.md with dispositions.
- done when: example indexed, lessons landed.

### E1. Inception system
- phase: E · playbook: PB-E03 · claims: `inception/`
- INCEPTION.md (phases A to E), INTERVIEW.md (challenge steps),
  WG-EOS-001 venture scale, WG-EOS-002 repo shape (worked rulings from
  the estate).
- done when: module-shape rules hold, wargames indexed.

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
  from WiseWattage, PatterTech_Business, AutoWatt ADRs. ADR template.
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

- (none)

## Done

- A. Phase A: migration, roots, governance, registries, org instance,
  check tool (session S-0001, 2026-07-07).
