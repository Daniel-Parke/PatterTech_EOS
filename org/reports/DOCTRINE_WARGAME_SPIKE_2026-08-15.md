---
summary: Non-merging architecture and data-analytics spike for the Doctrine and Wargaming ontology
type: org
tags: [eos, wargame, arch, data]
---

# Doctrine and Wargaming two-pack spike

This is the acceptance spike required by T-0026 before the governance records
can be accepted. It changed no pack, identifier or derived view. It read the
architecture and data-analytics packs from pinned commit
`7f56e4e22378323cf58318fe051d26b5afa8c35f`, transformed them in memory, and
discarded the result.

The pair is deliberately awkward. It includes binding, default and preference
material, legacy `WG-*` records, newer `GD-*` records, and the live collision
between `GD-ARCH-001` and `WG-ARCH-001`. It contains 39 normative source
blocks and 14 procedures. Twenty-two other pack files make 140 references to
the two packs' legacy labels, so the compatibility claim has a real surface.

## Prototype contract

The prototype assigned one temporary `DOC-*` identity per source block in
stable source order. It moved the complete block into the atom, replaced the
pack occurrence with an explicit HTML compatibility anchor and a DOC link,
and generated a summary view by sorting on full ID. It did not infer identity
from the numeric tail, so `GD-ARCH-001` and `WG-ARCH-001` remained separate.

The experiment counted the old full-pack route in UTF-8 bytes. The proposed
route counted the two reduced pack routers plus all 39 doctrine summaries, the
information matching would load automatically. Full doctrine bodies remained
on demand.

## Results

| Gate | Result |
| --- | --- |
| Source coverage | 39 blocks: 6 requirement, 23 default and 10 preference |
| Stable identities | 39 unique temporary DOC IDs; all 14 existing procedure IDs and paths unchanged |
| Collision | `GD-ARCH-001` and `WG-ARCH-001` resolved as separate records |
| Pinned resolution | Every pilot procedure path resolved at the pinned commit |
| Compatibility | 39 explicit anchor aliases generated, including synthetic preference anchors |
| Single normative source | No complete migrated source block remained in the simulated pack routers |
| Determinism | Rendering from forward and reverse input order produced identical bytes |
| Generated-view hash | `0024a9a5b6812e46a42c6901cf210e78fb9aa331fd6fb6ea681931ff1ecd43a5` |
| Context | 41,966 bytes before; 32,355 bytes after |
| Context delta | 9,611 bytes smaller, a 22.90 per cent reduction |

## Ruling

The ontology is viable with four constraints.

1. Existing `GD-*` and `WG-*` identities and paths stay immutable. Their
   prefixes are historical identity, not the semantic type.
2. Atomic DOC files are canonical. Pack bodies retain activation, outcomes,
   non-goals, compatibility maps and decision maps, not a second copy of the
   standing rules.
3. Compatibility needs explicit anchors and resolver aliases. Bold labels are
   not fragment anchors and cannot carry the migration alone.
4. The full 501-row migration ledger and shared resolver must land before a
   pack is rewritten. A syntax-only extraction is not allowed to decide
   authority, splitting, merging or rejection.

The spike proves the acceptance conditions for the ontology decision. It does
not claim the temporary atom allocation is final, and none of its temporary
IDs entered the working tree.
