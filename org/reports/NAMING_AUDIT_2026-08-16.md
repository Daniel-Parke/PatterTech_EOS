---
summary: Independent frozen-baseline and red-oracle audit for the T-0028 naming migration
type: org
tags: [eos, testing]
---

# T-0028 naming audit

## Scope

This is the independent pre-implementation oracle for T-0028. It reads the
machine baseline rather than repeating the migration inventory in test code.
The source tree is commit `b6f6a2b1861c64804ca9a7524d19e588e2e6901c`.
The reassigned claim set is commit
`ca1a2d2e86bc98f1810bf68a6889eef37b5cadc0`.

## Baseline result

The baseline agrees with the frozen source tree: 1,985 tracked files, 25 stable
pack slugs, 516 Doctrine records, 127 Wargames, 19 relations and 103 explicit
identity migrations. All target identities and paths are unique. None reuse a
reserved retired identity.

The three frozen inventory hashes were reproduced exactly:

| Inventory | SHA-256 |
| --- | --- |
| Wargame identity and path rows | `9ad902bc0785c1bd416cfd3be83fc27e0d1076335a7529e5723734bb0308f591` |
| Relation identity and path rows | `74e711329ee2f27d543ac95604620564e7f58eba585be40afee34015dcc32773` |
| Combined typed rows | `7391522c25d563eb69f3c356814ec12315d5b5572e5530c7559554a4f7ee92ad` |

Two corrections were made during review. The claim commit now names the
reassignment commit, and the pack contract calls its namespace field
`id_namespace` consistently.

## Oracle result

`python -m pytest tests/test_naming_oracle.py -q -k baseline` passes with one
test passed and seven target tests deselected.

The full isolated oracle is intentionally red before implementation: one test
passes and seven fail. The failures separately identify missing pack metadata,
the old collection layout and public names, the absent canonical Wargame and
alias map, missing semantic migration targets, the old lesson disposition,
overlong or mid-word Doctrine basenames, and 410 live files outside the
approved historical surfaces that still use pre-contract naming.

The oracle also requires current aliases and resolution, resolution at the
frozen commit, exact relation movement, and semantic equality after only the
approved naming substitutions. This prevents a mechanically tidy migration
from silently changing a decision procedure.

## Artefact hashes

| Artefact | SHA-256 |
| --- | --- |
| `org/migration/NAMING_BASELINE.json` | `985680c6841323b506919cc18540212c0438712a5c911b8b57bb595f5454ae6a` |
| `tests/test_naming_oracle.py` | `114c7ac3f9c16eff592f6a6a05c76ea5b40854ee6539484d10fedd010c240ee7` |

These hashes freeze the independently reviewed baseline and oracle before the
implementation lane begins.
