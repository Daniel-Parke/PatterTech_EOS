---
summary: The law of eos-mini, front-matter schema excerpt, tag vocabulary and the supersession rule
type: governance
tags: [eos]
---

# GOVERNANCE

The contracts every file in this fixture obeys. It is an excerpt of
the full EOS governance, cut down to what the benchmark tasks touch.

## Front-matter schema

Every markdown file opens with a YAML block carrying at least
`summary`, `type` and `tags`. Types used here: `root`, `governance`,
`org`, `doctrine`, `wargame` and `index`. Wargames also carry `status`
and `review_by` (YYYY-MM). Derived files carry `derived: true` and are
regenerated with `python tools/eos_check.py --write-index`, never
edited by hand. Lineage, when it exists, is carried by `supersedes`
and `superseded_by` and must be bidirectional.

## Tag vocabulary

Tags outside this list fail check E009. Add a tag by editing this
list in the same change that first uses it.

- `eos`: the operating system itself
- `web`: web design and front-end
- `content`: content pipelines
- `tooling`: scripts and checks
- `wargame`: decision procedures

## Supersession

Guidance is retired by lineage, not deletion. When a newer ruling
replaces an older file, the link is explicit and bidirectional: the
old file gains `superseded_by: <path>` in its front-matter and the
replacement carries `supersedes: <path>` back to it, both in the same
change. A superseded file keeps its place in the tree so the history
stays legible, and it must no longer be cited as active guidance.
