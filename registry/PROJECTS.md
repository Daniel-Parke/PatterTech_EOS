---
summary: The venture directory, what each is pinned to, whether that pin resolves, and when it was last checked
type: registry
tags: [eos]
status: active
review: 2026-11
---

# PROJECTS

Every venture the EOS serves. One row appended at each Session 0 close,
the one sanctioned cross-repo write.

**A pin must resolve to a pushed tag or to a commit reachable from
origin.** Check S010 enforces it: it resolves every recorded commit and
fails the row if the object is missing or is reachable from nothing that
was ever pushed. A pin naming a version is not evidence that the version
exists; the tag is. Scale is recorded as the venture was seeded, and v2
merges M and L into ORG at the next recompile.

| Venture | Path | Scale | EOS pin | Pin resolves | Packs adopted | Status | Last verified | Last harvest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Venture A | `C:\Users\Daniel\Documents\Coding\Github\Venture A` | L | pre-1.0.0 @ 0a2a044 | Yes. 0a2a044 is an EOS commit of 2026-07-07 and an ancestor of both pushed tags, v1.0.0 and archive/v1-final | None. The pin predates the pack system, so the venture carries v1 doctrine only | Rubric signed 2026-07-07, Genesis in progress. Seed merged to Venture A main at bc34018 | 2026-07-07 | Never. PB-E02 has not run; the 2026-07-07 reseed feedback fold predates the cadence |
| Guth | `C:\Users\Daniel\Documents\Coding\Github\Project_Guth` | M | recorded as "v1.0.0 @ 3807eb1" | Partly, and the label is wrong. 3807eb1 resolves and is reachable from the pushed tag archive/v1-final, but **it is not the v1.0.0 tag**: v1.0.0 is 85b31f4 of 2026-07-07, and 3807eb1 is a 2026-07-08 branch commit made after it. The pin normalises to archive/v1-final at the next upgrade | None. Same reason as Venture A | Rubric signed and the S0 gate passed 2026-07-15. Genesis complete, S1 next | 2026-07-15 | Never |
| PatterTech_Website | `C:\Users\Daniel\Documents\Coding\Github\PatterTech_Website` | S | pre-EOS, no pin | Not applicable. The venture predates the EOS and was never compiled from it | None | Live. The v4 pass shipped; current work sits on branch feat/foundations-pass. It aligns to a compiled S seed when that work settles, no earlier | 2026-08-03 | Never |

Notes:

- **What the 2026-08-03 pass checked.** A read-only look at each repo's
  git state, nothing written. It established branch tips and confirmed
  the pin facts above. It did not re-verify Genesis progress in Venture A
  or Guth, so those rows keep their earlier verification dates.
- Venture A's seed pack is the extraction source for `kernel/templates/`.
  It reseeds from the v2 kernel before Genesis completes (Daniel's
  ruling, ADR-0001 section 12); the pin predates the v2 kernel freeze,
  so its route is recompile rather than upgrade.
- The three rows above are the governed ventures. Every other repo in
  the estate is an inventory row in `estate/repos.json` with
  `governed: false`, and the quarterly estate review asks adopt or defer
  for each.
- No venture has been harvested under PB-E02. The lesson rows already in
  `registry/LESSONS.md` came from the pre-cadence estate survey and the
  Venture A reseed feedback, and they say so.
