---
summary: The venture directory, what each is pinned to, whether that pin resolves, and when it was last checked
type: registry
tags: [eos]
status: active
review: 2026-11
---

# PROJECTS

Every venture the EOS has seeded or adopted. One row appended at each
Session 0 close, the one sanctioned cross-repo write.

**This is a directory of what was seeded, not a compliance register.**
Under ADR-0006 the EOS compiles a seed and a blueprint and then stops.
A venture diverges freely and owes the EOS nothing, and the EOS never
initiates a check on one. So a row says what was true when the venture
was born and when someone last looked. It is not a claim about how the
venture is run today. A stale status line here is a stale reading, not
a venture in breach of anything.

**A pin must resolve to a pushed tag or to a commit reachable from
origin.** Check S010 enforces it: it resolves every recorded commit and
fails the row if the object is missing or is reachable from nothing that
was ever pushed. A pin naming a version is not evidence that the version
exists; the tag is. Scale is recorded as the venture was seeded, and v2
merges M and L into ORG at the next recompile.

**Genesis in the rows below means v1's PB-001**, the playbook a
venture's own organisation ran to produce its design set. That is
history, at the archive/v1-final tag. `inception/GENESIS.md` defines
what the word means from v2.1 on, a single compiled phase run once in
the venture repo after the seed gate, and no venture in this table has
run it.

| Venture | Path | Scale | EOS pin | Pin resolves | Packs adopted | Status | Last verified | Last harvest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Venture A | `C:\Users\Daniel\Documents\Coding\Github\Venture A` | L | pre-1.0.0 @ 0a2a044 | Yes. 0a2a044 is an EOS commit of 2026-07-07 and an ancestor of both pushed tags, v1.0.0 and archive/v1-final | None. The pin predates the pack system, so the venture carries v1 doctrine only | v1 Genesis was in progress on 2026-07-07, the day the rubric was signed, and nothing has observed the venture's progress since. Read that as an observation over a month old, not as a current status. Seed merged to Venture A main at bc34018 | 2026-07-07 for venture progress. The 2026-08-03 pass re-read git state only | 2026-08-08. Nothing new: both entries had already been folded during the v1 build |
| Guth | `C:\Users\Daniel\Documents\Coding\Github\Project_Guth` | M | recorded in the venture as "v1.0.0 @ 3807eb1", and the version label is wrong: v1.0.0 is 85b31f4 | The commit resolves; the label does not. 3807eb1 is a 2026-07-08 branch commit, reachable from the pushed tag archive/v1-final. The v1.0.0 tag is 85b31f4 of 2026-07-07, an earlier commit, so the venture is pinned past v1.0.0 and calls it v1.0.0. Treat the pin as the commit and ignore the label. It normalises to archive/v1-final at the next upgrade, which has not happened | None. Same reason as Venture A | v1 Genesis was recorded complete on 2026-07-15, the day the rubric was signed and the S0 gate passed, with S1 next. Nothing has observed the venture since | 2026-07-15 for venture progress. The 2026-08-03 pass re-read git state only | 2026-08-08. Fifteen entries and a matured stack profile, the substance of the harvest |
| PatterTech_Website | `C:\Users\Daniel\Documents\Coding\Github\PatterTech_Website` | S | pre-EOS, no pin | Not applicable. The venture predates the EOS and was never compiled from it | None | Live. The v4 pass shipped; current work sits on branch feat/foundations-pass. It aligns to a compiled S seed when that work settles, no earlier | 2026-08-03 | 2026-08-08. No feedback file: the venture predates the template, which is itself a finding |

Notes:

- **What the 2026-08-03 pass checked.** A read-only look at each repo's
  git state, nothing written. It established branch tips and confirmed
  the pin facts above. It did not re-verify venture progress in Venture A
  or Guth, so those rows keep their earlier verification dates and both
  status lines are older than a month. Neither venture owes the EOS an
  update. Under ADR-0006 a check-in is the venture's to start, and the
  EOS applies nothing from it.
- Venture A's seed pack is the extraction source for `kernel/templates/`.
  Its pin predates the v2 kernel freeze, so its route is recompile
  rather than upgrade (Daniel's ruling, ADR-0001 section 12). No v2
  reseed has run, and the EOS will not push one: under ADR-0006 the
  venture reseeds if and when the venture wants to.
- The three rows above are the seeded and adopted ventures. Governed is
  the manifest's word for that, and after ADR-0006 it means the EOS
  compiled or adopted the repo and holds its pin, not that the EOS rules
  it. Every other repo in the estate is an inventory row in
  `estate/repos.json` with `governed: false`. The estate review asks
  adopt or defer for each, and under ADR-0008 it runs when a repository
  is added or a seed is compiled rather than on a quarterly clock.
- The first PB-E02 harvest ran on 2026-08-08 against all three ventures.
  Guth's feedback file was the substance of it, Venture A's two entries
  had already been folded during the v1 build, and PatterTech_Website
  ships no feedback file at all. The other rows already in
  `registry/LESSONS.md` came from the pre-cadence estate survey and the
  Venture A reseed feedback, and they say so.
