---
summary: Daniel's manual for running the EOS, launchers, rhythm and troubleshooting
type: guide
tags: [eos]
review_by: 2027-07
---

# OPERATORS_GUIDE

How Daniel runs the EOS. Agents read this to understand what the human
does; Daniel reads it to know what to launch and when.

## The sixty-second model

The EOS is a repo that seeds ventures and learns from them. You launch
sessions against it; each session boots from files, does one queued
thing, and closes out so a stranger could continue. One EOS session at
a time (WIP is 1): check `org/STATE.md` says no other session is active
before launching.

## Launchers

Paste one line into a fresh agent session in this repo:

- **E1, build**: "Read AGENTS.md, entry mode 2, continue the build."
  The workhorse until v1.0.0 ships.
- **E2, Session 0**: "Read AGENTS.md, entry mode 3. The new venture is
  <one line>. Repo at <path>." Run from the venture repo once
  inception/ is populated (Phase E).
- **E3, harvest**: "Entry mode 2, run PB-E02 harvest." Monthly after
  v1.0.0.
- **E4, hygiene**: "Entry mode 2, run PB-E09 hygiene." Monthly.
- **E5, promotion review**: "Entry mode 2, run PB-E04." Monthly.
- **E6, release**: "Entry mode 2, run PB-E05 release." On demand.
- **E7, drill**: "Entry mode 2, run PB-E07 inception drill." Quarterly.
- **E8, upgrade a venture**: "Entry mode 2, run PB-E06 for <venture>."

## Rhythm

- **While building v1.0**: launch E1 whenever you have a slot; review
  the commits; answer anything flagged in `org/STATE.md`.
- **Monthly after v1.0.0**: E3, E4, E5 (roughly thirty minutes of your
  review time). Cadence table in `org/CADENCE.md`; a due cadence
  outranks new low-priority work.
- **Quarterly**: E7 drill, and the projects-registry review (who is
  pinned to what, who is more than one minor version behind).

## Your gates

Only you can: approve ADRs and anything touching the protected set,
sign the human items of a seed rubric at a Session 0 gate, approve
doctrine promotions and deviations, create remotes and accounts, spend
money.

## Troubleshooting

- **STATE disagrees with reality**: reality wins. Fix STATE, note it in
  the session log.
- **`active_session` is set but nothing is running**: a session died
  without closing out. Read its log if it wrote one, clear the line,
  note it.
- **A check keeps failing**: the three-strikes rule applies to you too.
  After three distinct attempts, stop and read the failure properly.
- **INDEX.md looks wrong**: never hand-edit it. Fix front-matter, then
  `python tools/eos_check.py --write-index`.
- **The folder rename** (end of the build): close every session and
  editor rooted in the repo, then from the parent directory run
  `Rename-Item PatterTech_Framework PatterTech_EOS`, update the two
  references in PatterTech_Website, create the private GitHub repo and
  push with tags.
