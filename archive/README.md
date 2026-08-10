---
summary: Where v1 lives now, how to retrieve any file from it, and why it is not in the working tree
type: index
tags: [eos]
---

# ARCHIVE

The archive of record is a pushed tag, not a directory (ADR-0003).

The complete v1 tree, one hundred and forty-two files, is at
`archive/v1-final`. The founding release is at `v1.0.0`. Both are pushed
to origin, so a fresh clone can reach either without this directory
existing.

## Retrieving a v1 file

```bash
git show archive/v1-final:doctrine/web-design/DOCTRINE.md
```

To list what is there:

```bash
git ls-tree -r --name-only archive/v1-final
```

To check a whole v1 tree out somewhere harmless:

```bash
git worktree add ../eos-v1 archive/v1-final
```

## Why the tree is going

Keeping it costs more than it buys. Forty-nine live files reference
`archive/v1/` and twenty-three of those are inside `packs/`, so an agent
following a live pack's own decision map lands on a file stamped
`status: archived` and reads it as current law. A third of `INDEX.md`
was archived material and benchmark fixtures, and two fixture wargames
had reached the live guide index and were being served as EOS guidance.
The indexes are fixed. The references are not, yet.

The rule that put this material here was written to protect history.
History is better protected by a tag, which cannot drift and cannot be
mistaken for current law by anything that walks the working tree.

## The ordering rule, and where this stands

Nothing is retired until every live reference to it is resolved. Where a
live pack delegates a decision into an archived wargame, the fix is to
write the guide in the pack, never to delete the target and leave a
dangling link. That is recorded in `GOVERNANCE.md` under "Staleness and
supersession" and it is binding.

`archive/v1/` is therefore still in the tree while those references are
migrated. It is no longer indexed, so nothing routes an agent into it.
The largest outstanding piece is `packs/architecture/PACK.md`, whose
decision map delegates five forks to `WG-ARCH-002` through `006`; those
guides have to be written into the pack before the tree can go.
