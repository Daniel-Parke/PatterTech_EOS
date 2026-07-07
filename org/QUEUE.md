---
summary: The ordered build queue for the EOS, phases B to F and the release
type: org
tags: [eos]
---

# QUEUE

The EOS's work queue, ordered. A build session (entry mode 2) takes the
top unblocked item, follows its playbook, and closes out. One item per
session unless items are trivially small. WIP is 1. The v1.0 build is
complete bar REL's manual close; Venture A is signed and in Genesis.

## Ready

### G1. Test-doubles wargame (WG-DEL-005) and doctrine line
- phase: post-1.0 · playbook: PB-E03 · claims: `doctrine/delivery/`
- When fake against mock against real, per port; verified-fakes
  (contract suites over both adapters) as the decision rule's spine;
  Venture A's ADR-0003 as the first argued ruling. One delivery
  DOCTRINE line citing it.
- Hold until Venture A's W1 foundation orders are moving (Daniel's
  scheduling ruling, 2026-07-07).
- done when: wargame indexed, budgets hold, doctrine line cites it.

### G2. Hexagonal boundary statement in the architecture module
- phase: post-1.0 · playbook: PB-E03 · claims: `doctrine/architecture/`
- Ports at every vendor and IO seam; the domain never imports adapters;
  the config-only against code-port boundary distinction. Likely a
  WG-ARCH-007 sharpening plus one doctrine line rather than a new
  wargame; decided when argued. Venture A ADR-0003 is the worked
  material.
- Hold as G1.
- done when: argued, indexed, budgets hold.

## Blocked

### REL. Release v1.0.0: awaiting Daniel's manual close
- phase: release · playbook: PB-E05 · session S-0018
- Checks green, CHANGELOG v1.0.0 entry written, tag v1.0.0 created
  locally. Blocked on the manual close: folder rename to
  PatterTech_EOS, the two PatterTech_Website reference updates, the
  private GitHub remote, push with tags, PROJECTS rows updated with
  the new home (commands in OPERATORS_GUIDE troubleshooting).
- done when: tag pushed, PROJECTS rows note the new home.

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
- D1. Venture A reseed: compiled S-0008, rubric signed by Daniel and
  merged to a single main (bc34018) at S-0019, 2026-07-07; Genesis
  unblocked.
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
