---
summary: What the evidence supports for the architecture pack, three contrasting philosophies with fit conditions, and the binding versus default versus preference split
type: example
tags: [eos]
---

# Architecture research notes

Cutoff 2026-08-03. Eighteen new sources in `sources.fragment.json`,
plus the architecture evidence already in the ledger: MADR (EV-0097),
ddd-crew Bounded Context Canvas, Context Mapping and Starter Modelling
Process (EV-0098, EV-0099, EV-0100), C4 (EV-0101), Structurizr DSL
(EV-0102), OpenAPI (EV-0023), AsyncAPI (EV-0024), JSON Schema
(EV-0025), dbt model contracts (EV-0057), Stripe API versioning
(EV-0061), Pact (EV-0091), Testcontainers (EV-0093), SLSA (EV-0038),
OPA (EV-0071), METR RCT (EV-0010).

## The three philosophies, and when each fits

### 1. Deployment-shaped: services as the unit of boundary

A boundary is a process boundary. Independence is bought with the
network: separate deployables, separate databases (FRAG-17), sagas for
cross-service writes, contract tests at every seam (EV-0091).

Fits when there are genuinely separate owners who must ship without
coordinating, when one component has a volume or hardware profile the
rest does not, or when a regulatory or blast-radius argument forces
isolation. Uber's DOMA (FRAG-15) is what this looks like when it works
at scale, and the tell is instructive: at 2,200 services they had to
reimpose domains, a five-layer call rule and per-domain gateways to
recover the discipline a single deployable gives away.

Anti-patterns: the networked monolith, services that look independent
but must be released together (FRAG-15); splitting before boundaries
are known, which buys the wrong boundary at the highest price
(FRAG-08); treating the shared-database label as an argument for
separate servers when separate credentials on private tables enforce
the same ownership (FRAG-17).

### 2. Module-shaped: modular monolith, one deployable

Boundaries are logical and enforced in the build. One process, one
database, declared module interfaces, and a rule engine that fails the
build on a crossing (FRAG-01, FRAG-02, FRAG-03). Shopify (FRAG-14) is
the large-scale existence proof; Service Weaver (FRAG-07) is the
argued version, naming the defect as conflating logical with physical
boundaries and reporting up to 15x latency and 9x cost improvement
from co-locating the same modules.

Fits nearly every venture at inception: one or two people, one
release train, boundaries still being discovered. It keeps the split
option open because the module graph is the thing you would split
along.

Anti-patterns: modules declared in documentation only, with no
machine check, which the mirroring evidence (FRAG-09) predicts will
collapse toward the shape of the team; progressive isolation scores
that tolerate violations rather than blocking them, which is a
migration tactic for legacy mass and not a greenfield rule (FRAG-14).

### 3. Contract-shaped: ports, adapters and generated seams

The boundary that matters is the one you can substitute or regenerate:
a port with more than one plausible driver or device (FRAG-05),
schema-first contracts (EV-0023, EV-0024, EV-0025), generated and
committed clients with a drift gate, vendor adapters with the raw
protocol owned at the wire (FRAG-16, EV-0061).

Fits where substitution is real: two drivers (HTTP and a job runner),
two devices (a vendor and its replacement), or a handover obligation.
It composes with either of the other two rather than competing.

Anti-patterns: an adapter per dependency where no second device is
plausible, which is the ceremony reading of hexagonal that the 2005
source never bounded (FRAG-05); a typed client that ignores
`response.ok`; letting a framework parse a webhook body before the
HMAC is checked over the raw bytes (FRAG-16).

## Disagreements worth recording

- **Does splitting help or hurt?** Fowler (FRAG-08) says monolith
  first, on stated anecdote, and says so tentatively. Service Weaver
  (FRAG-07) reports large wins from co-location but is a workshop
  position paper with the authors' own benchmark and no independent
  replication. DORA (FRAG-06) refuses the argument outright: the
  label does not determine the outcome, since organisations fail with
  microservices and succeed with mainframes. The resolvable form is
  DORA's: measure independent deployability, isolated testability and
  upstream-caused unplanned work, not process count.
- **Is a shared database an anti-pattern?** FRAG-17 names it one,
  then proposes private tables with distinct credentials in a single
  database as a legitimate isolation level. The disagreement is
  vocabulary: uncontrolled access is the defect, physical colocation
  is not.
- **Static or runtime boundary checks?** Import-graph tools
  (FRAG-02, FRAG-03) and bytecode tools (FRAG-01) miss reflection,
  dependency injection and string-keyed lookup. Shopify's answer was
  call graphs from CI runs (FRAG-14). Neither alone is sufficient,
  and the honest position is that static checking is the cheap
  default and dynamic wiring is the known blind spot.
- **How much architecture description?** ISO/IEC/IEEE 42010:2022
  (FRAG-13) gives the rigorous vocabulary; arc42 (FRAG-04) gives
  twelve sections; C4 (EV-0101) gives four diagrams. arc42's own
  canvas exists because its full template is too heavy, which is
  evidence that section-complete templates invite box-filling.

## Suggested binding rules, defaults and preferences

**Binding** (evidence strong enough to fail a build):

1. Declared boundaries are machine-checked from the first week, in a
   named tool with a committed contract file (FRAG-01, FRAG-02,
   FRAG-03). A rule with no red build does not exist (FRAG-09
   supplies the reason: the artefact drifts toward the team shape).
2. Builds are deterministic and verified by rebuilding, not by
   inspection. Where timestamps are embedded, SOURCE_DATE_EPOCH rules
   apply exactly as written (FRAG-10); tools are pinned by version or
   hash rather than taken from the host (FRAG-11).
3. Decisions that close a door are recorded as MADR ADRs (EV-0097)
   naming options, why each lost, and consequences accepted. Agents
   have no memory across sessions.
4. Vendor webhooks are verified over raw bytes with a bounded
   recency window before any parsing (FRAG-16).
5. Generated contract artefacts are committed with a drift gate
   (EV-0023, EV-0024, EV-0025, EV-0057).

**Default** (chosen unless an ADR argues otherwise):

- One deployable, one database, modules enforced in the build
  (FRAG-07, FRAG-14, FRAG-08).
- Boundary tooling matched to the stack: import-linter layers for
  Python, dependency-cruiser for TypeScript, ArchUnit for JVM.
- C4 container and component views authored in Structurizr DSL
  (EV-0101, EV-0102), and arc42 headings borrowed only for the
  non-diagram content the pack actually needs (FRAG-04).
- Outbox for any state change that must produce a message, with
  idempotent consumers (FRAG-12).
- Split only when a measured DORA-shaped signal appears: changes
  blocked on another owner, inability to test in isolation, or
  upstream-caused unplanned work (FRAG-06).

**Preference** (author's taste, argue freely):

- Bounded Context Canvas and Context Mapping as the discovery
  artefacts before a boundary is declared (EV-0098, EV-0099,
  EV-0100).
- Naming the specific event pattern in use rather than saying
  event-driven, since the four have different costs (FRAG-18).
- Ports created only where a second driver or device is plausible
  (FRAG-05).
- Domain and gateway grouping deferred until a service count makes
  it a real problem (FRAG-15).

## Applicability warning carried across the whole pack

Almost none of the empirical work here observed a one-person,
agent-assisted venture. DORA surveys team-scale and enterprise
organisations, the mirroring study observes firms and communities,
Shopify and Uber are hyperscale case reports, and Service Weaver is a
prototype benchmark. EV-0010 (METR) is the reminder that intuitions
about agent-era productivity have already been measured wrong once.
The pack should state its rules as rules for machine-enforced
boundaries in a small codebase, not as inherited enterprise practice.
