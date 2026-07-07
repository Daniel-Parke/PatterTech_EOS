---
summary: The north star, what the EOS is for and the invariants that hold as it grows
type: root
tags: [eos]
---

# Vision: the engineering operating system

This repo exists so that a capable agent, given only a high-level
description of a new venture, can plan, architect, implement, test,
document, deploy and evolve it to the standard of an experienced senior
PatterTech engineer, with Daniel supplying judgement at a few named
gates rather than repeating himself project after project.

It does this by externalising engineering judgement into files: doctrine
that has survived argument, wargames that pre-solve the forks every
project meets, a kernel of organisational machinery that compiles into
each venture, registries of what is true today, and a governance layer
that lets all of it improve without rotting.

The v0.1 plan of record (build the web-design module, then generalise
from the Venture A seed-pack work) is fulfilled. ADR-0001 records the
v1.0 architecture that replaced it. The build queue lives in
`org/QUEUE.md`; the module roadmap and extraction mandates live in
`doctrine/README.md`.

## What must stay true as the EOS grows

- **Agnostic core, locked-in ventures.** EOS files never assume one
  brand, stack or client. Each venture freezes its choices in its own
  lock-book. A rule that only makes sense for one venture belongs in a
  worked ruling or an example, not in doctrine.
- **Wargames before doctrine.** A rule earns its place by surviving the
  argument, not by being written confidently. Promotion has numbers, and
  demotion exists (GOVERNANCE.md).
- **Files over memory.** Everything an agent needs is in the repos.
  Session memory is a convenience, never the source of truth.
- **Doctrine argues; registries date.** Timeless rules and dated facts
  never share a file. Time-sensitive claims carry `review_by`, and stale
  guidance is a bug.
- **Ceremony tiers with the venture.** The smallest seed that fits. A
  brochure site gets six files, not a constitution.
- **Compiled, never composed.** Ventures are seeded by slot-filling
  hand-written templates, with a compile report proving ancestry.
- **Every venture feeds back.** Rulings and lessons are harvested,
  repeated rulings become defaults, hardened defaults become doctrine.
  The EOS grows from lived work instead of speculation.
- **Lean.** Capture the decision structure, not restatements of common
  knowledge. The EOS should stay fast to read and easy to extend.
