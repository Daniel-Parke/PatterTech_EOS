---
summary: Frozen inventory and performance baseline before the Doctrine and Wargaming rebuild
type: org
tags: [eos, wargame]
---

# Doctrine and Wargaming rebuild baseline

This is the frozen before-state for T-0026. The knowledge tree is taken from
`main` commit `7f56e4e22378323cf58318fe051d26b5afa8c35f`. The later task-record commit
does not change that knowledge tree.

The hashes below are SHA-256 over the sorted, unique rows, joined with LF and
terminated by LF. They let the migration prove that it accounted for the
starting estate without making this report a second copy of it. The full
inventory remains reconstructable from the pinned commit.

| Inventory | Definition | Rows | SHA-256 |
| --- | --- | ---: | --- |
| Doctrine anchors | `git grep -n` rows beginning with a bold `B`, `D` or `P` number in `packs/*/PACK.md` | 279 | `246923ab83bfcefb35fb97b4432503994a55b1db07e2d4102bd74f21f2af5b1a` |
| Live procedures | ID and path for Markdown under pack `guides/` and inception `wargames/` | 114 | `2d532914db4bc3ce91459f055656e54da31b69cfc54fe8fd269726d766052dda` |
| Procedure references | Every tracked Markdown or JSON row containing a `GD-*` or `WG-*` reference | 949 | `813085d0400458f2b276a8e569c58eb2d8e6544047b2a207855a5e27bdc28834` |
| Retired procedures | ID and archived path from `archive/RETIRED_IDS.json` | 22 | `cc17485e40e06626e572a62c8037578f5c759b35bdc99369a3301567e8cfeb36` |

The 279 anchor rows are deliberately an occurrence inventory, not a claim
that 279 doctrines exist. Some packs discuss an old numbered rule again in
their counter-evidence. The migration ledger must give every occurrence a
disposition while assigning one canonical definition to the proposition.

## Live surface

| Measure | Before state |
| --- | ---: |
| Built packs | 25 |
| Decision procedures | 114, comprising 100 `GD-*` and 14 `WG-*` IDs |
| Evidence records | 562 |
| ADRs | 11 |
| Explicit file-level conflicts | 0 |
| Retired procedure IDs | 22 |

## Validation and timing

`python -m pytest -q` passed all 576 tests in 150.09 seconds.

Five warm local runs of `python -m tools.eos check --repo` took 2.552,
3.060, 2.733, 2.526 and 2.334 seconds. The median was 2.552 seconds, so the
accepted 20 per cent ceiling is 3.062 seconds under the same local conditions.
Every run reported 0 errors and the same pre-existing E004 warning in
`registry/LICENCE_RESIDUALS.md`.

## Reconstruction

The inventory definitions above are part of the freeze. Reconstruction must
use the pinned commit, not the working tree. References are counted by source
row rather than token. Doctrine anchors are counted by occurrence because
that exposes repeated compatibility anchors and historical discussion for
explicit disposition later.
