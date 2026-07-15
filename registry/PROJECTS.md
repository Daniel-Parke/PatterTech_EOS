---
summary: The venture directory, who is seeded from what and when last harvested
type: registry
tags: [eos]
status: active
review_by: 2026-10
---

# PROJECTS

Every venture the EOS serves. One row appended at each Session 0 close
(the one sanctioned cross-repo write). The quarterly review flags
ventures more than one minor version behind.

| Venture | Path | Scale | EOS pin | Status | Last harvest |
| --- | --- | --- | --- | --- | --- |
| Venture A | `C:\Users\Daniel\Documents\Coding\Github\Venture A` | L | pre-1.0.0 @ 0a2a044, merged to main at bc34018 (single branch) | Rubric signed 2026-07-07; Genesis in progress | 2026-07-07 (reseed feedback, two entries folded) |
| PatterTech_Website | `C:\Users\Daniel\Documents\Coding\Github\PatterTech_Website` | S | pre-EOS (v0.1 lock-in in docs/DESIGN_SYSTEM.md) | Live, v4 pass in progress | never |
| Guth | `C:\Users\Daniel\Documents\Coding\Github\Project_Guth` | M | v1.0.0 @ 3807eb1 | Rubric signed and S0 gate passed 2026-07-15; Genesis complete; S1 next | never |

Notes:

- Venture A's seed pack is the extraction source for `kernel/templates/`;
  it reseeds from the new kernel before Genesis runs (Daniel's ruling,
  ADR-0001 section 12).
- PatterTech_Website predates the EOS; its design system doubles as the
  v0.1 worked example (`examples/pattertech-website.md`). It aligns to a
  compiled S-scale seed when the v4 pass settles, no earlier.
