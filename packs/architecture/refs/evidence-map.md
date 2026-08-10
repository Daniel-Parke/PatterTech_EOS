---
summary: Which evidence row supports which requirement, what population it observed, and where its licence limits reuse to paraphrase
kind: fact
scope: estate
sources: [EV-0010, EV-0023, EV-0024, EV-0025, EV-0057, EV-0061, EV-0097, EV-0098, EV-0099, EV-0100, EV-0101, EV-0102, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163]
volatility: slow
review: 2027-04
type: example
tags: [arch, content]
---

# Evidence map

Every source this pack rests on lives in `registry/evidence.json` with
its version, licence, access date and review trigger. This file maps
the ids to the claims and records what each source is not allowed to
carry. Version, licence and access date are not restated here, because
the ledger owns them and a second copy would drift.

## Claim to source

| Claim | Sources | Grade |
| --- | --- | --- |
| A boundary contract in CI is the cheapest enforcement | EV-0146, EV-0147, EV-0148 | maintainer documentation |
| Undeclared boundaries drift toward the org shape | EV-0154 | matched-pair study, correlational |
| Decision records scale with the decision | EV-0097 | maintainer documentation |
| Determinism is bought by naming and clamping non-determinism | EV-0155, EV-0156 | standard plus vendor documentation |
| Generated contracts need a drift gate | EV-0023, EV-0024, EV-0025, EV-0057 | specifications plus one exemplar |
| Webhook signatures verify over raw bytes with bounded recency | EV-0161 | vendor documentation, paraphrase only |
| Payload versions are pinned at event creation | EV-0161, EV-0061 | vendor documentation |
| Logical and physical boundaries are separate decisions | EV-0152 | position paper, authors' own prototype |
| Boundaries are discovered, not designed | EV-0153 | explicitly anecdotal |
| Coupling is measured by outcomes, not by label | EV-0151 | cross-sectional survey, correlational |
| One process can hold boundaries at very large scale | EV-0159 | single-company case report |
| Many services reimpose structure at scale | EV-0160 | single-company case report |
| Ownership and physical separation are different prices | EV-0162 | pattern catalogue, no measurement |
| Outbox gives send-if-and-only-if-committed | EV-0157 | pattern catalogue, no measurement |
| A view answers a named stakeholder concern | EV-0158 | international standard, abstract only |
| Diagrams are a minority of an architecture record | EV-0149 | template, in use since 2005 |
| Diminishing obligation down the C4 levels | EV-0101 | single-author practice framework |
| One model generates many non-drifting views | EV-0102 | maintainer documentation |
| A port earns its existence at the second driver or device | EV-0150 | 2005 pattern statement, no evaluation |
| Four different patterns hide behind event-driven | EV-0163 | definitional essay, no measurement |
| Discovery artefacts before declaring a boundary | EV-0098, EV-0099, EV-0100 | maintainer documentation |
| Agent-era productivity intuitions have inverted before | EV-0010 | randomised controlled trial |

## Population limits worth repeating

The pack states this once and it is worth restating wherever a rule
gets quoted out of context:

- **EV-0151** surveys mostly team-scale and enterprise organisations,
  self-reported, cross-sectional, with no effect sizes on the page.
  Very little of that population resembles a venture of one to three
  people.
- **EV-0154** studies large organisations and open source communities.
  Nothing in the sample is a one-person team or an agent-run codebase.
- **EV-0159** and **EV-0160** are single-company reports at hyperscale
  with no counterfactual and self-reported outcomes.
- **EV-0152** is a workshop position paper. Its co-location figures
  come from the authors' own Go prototype and example workloads, with
  no independent replication.
- **EV-0153** states its own limit: the author lacks enough cases and
  calls any advice on the question tentative.
- **EV-0010** measured a 19 per cent slowdown against a believed 20
  per cent speed-up on mature repositories with early-2025 tooling. It
  is a caution about self-report, not a claim about 2026 agents.

None of these results may be promoted to universal doctrine. Where a
rule in this pack binds, it binds because of a documented protocol
requirement, a standard, or an estate decision, never because a
benchmark on a different population came out well.

## Licence constraints on reuse

Extract principles and write them in our own words. Reproduction is
not permitted from these rows:

- **EV-0158** is proprietary ISO material, read as a public catalogue
  abstract only. Vocabulary may be named; text may not be reproduced.
- **EV-0161** is proprietary vendor documentation. Paraphrase only,
  and its constants do not transfer to other vendors.
- **EV-0149, EV-0150, EV-0153, EV-0157, EV-0159, EV-0160, EV-0162 and
  EV-0163** carry site copyright with no open licence stated.
  Paraphrase only.
- **EV-0098** is CC BY-SA 4.0, so a derived canvas carries the
  share-alike obligation.
- The remainder are permissive or CC BY and may be quoted with
  attribution, though this pack still prefers extraction to quotation.

## Review triggers

Each row carries its own trigger in the ledger, and several are
on-change-of rather than dated: the boundary tools on their major
versions, SOURCE_DATE_EPOCH on a specification revision above 1.1,
ISO 42010 on a third edition, the Stripe seam on a signature scheme
beyond v1, and EV-0152 on any independent replication of its
co-location result. That last one is the trigger most likely to change
D1 of `packs/architecture/PACK.md`.
