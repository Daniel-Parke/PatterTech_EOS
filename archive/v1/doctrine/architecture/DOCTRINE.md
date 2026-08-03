---
summary: The seven binding architecture rules, argued by the estate's ADRs and the WG-ARCH wargames
type: doctrine
tags: [arch]
status: archived
---

# Architecture doctrine

Binding on every venture the moment its scale ruling gives it more
than one module. Each rule stands on wargame argument and estate
receipts; the wargame stays alive beneath its rule as the argument of
record.

1. **Boundaries are records, not conventions.** The layering lives as
   a machine-checked contract from the first week (WG-ARCH-001), and
   the directory tree grows to match it once a canary proves moves
   safe. A boundary an agent can cross without a red build does not
   exist.

2. **Decisions that close doors are ADRs.** Options considered, the
   reason each lost, consequences accepted, anti-patterns guarded.
   Immutable once accepted; reversal is a superseding ADR. Agents have
   no memory between sessions; the record carries the why, or the why
   is gone.

3. **Nothing generative in a build step.** Builds are deterministic:
   same inputs, same bytes. Agents plan and author; compilers and
   builders only transform. Where output is deterministic, pin it with
   a content hash and make re-baselining a deliberate reviewed event
   (WG-ARCH-006).

4. **Generated artefacts are committed and drift-gated.** Schemas,
   types, clients: generated offline, committed, and a CI gate fails
   when the committed copy lags the source (WG-ARCH-005). A failed
   mutation must never masquerade as success; typed clients check
   `response.ok` or they are not clients.

5. **One writer per fact.** Every fact has one upstream home and any
   number of links to it; a fact living in two places is a future
   disagreement. Derived values are computed, not stored, with the
   owned-cache and immutable-snapshot exceptions of WG-ARCH-003.

6. **Vendors are guests with departure plans.** Identity, money and
   anything handover-bound sit behind adapters the venture owns, exit
   routes written down; webhook verification is raw protocol, never an
   SDK (WG-ARCH-007). The venture's own database is the authorisation
   source of truth.

7. **Data topology is ruled, not accreted.** One database until a
   genuine second owner or a volume-asymmetric feed appears; records
   and readings never mingle (WG-ARCH-008). Every persisted table
   names its consumer and its retention plan before it lands.
