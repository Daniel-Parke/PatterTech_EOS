---
summary: Delivery module, six rules and four wargames on proof, gates and determinism
type: doctrine
tags: [delivery]
status: archived
---

# Delivery

The module that owns how work is proven: testing strategy, gate
design, coverage mechanics, visual regression, flake policy. Populated
at F2 from WiseWattage's delivery practice (CI workflows, coverage and
allowlist ratchets, pinned VRT, determinism fixes), the Venture A
acceptance-suite mandate and the v0.1 web-design QC gates.

## Activation triggers

Any venture with code and CI; the VRT fork activates with the first
styled component kit. S ventures without CI inherit the defaults and
run the lock-book's QC gates by hand until a rescale gives them a
pipeline.

## What lives where

- The six binding rules: `DOCTRINE.md`.
- The four forks: `wargames/` (WG-DEL-001 coverage level, 002
  end-to-end weighting, 003 VRT scope, 004 flake policy).
- Per-type procedures: the kernel playbooks PB-010 to PB-013, compiled
  into L ventures.
- Exact commands, thresholds and pinned versions: the venture's
  lock-book QC section and the stack profiles, never here.
