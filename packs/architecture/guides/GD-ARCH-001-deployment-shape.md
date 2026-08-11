---
summary: One deployable, several deployables, or contract-shaped seams inside one process
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0151, EV-0152, EV-0153, EV-0159, EV-0160, EV-0150, EV-0010]
review: 2027-03
type: guide
tags: [arch, infra]
---

# GD-ARCH-001: what shape is the deployment?

## The question

A boundary can be a process boundary, a build-enforced module
boundary, or a substitutable contract. The three are usually argued as
if they were one choice, and they are not. This fork is taken early,
paid for continuously, and reversed at high cost in one direction
only.

## It depends on

- Are there genuinely separate owners who must ship without
  coordinating? Not people who could, in principle.
- Does one component have a volume, hardware or cost profile the rest
  does not?
- Does a regulator, a contract or a blast-radius argument force
  isolation?
- Have the boundaries proved stable under change yet, or are they
  still guesses?
- Is a second driver or a second device genuinely plausible at this
  seam?

## Options

### A. Deployment-shaped

**What it is.** A boundary is a process boundary. Separate deployables,
separate stores, sagas for cross-service writes, contract tests at
every seam.

**Buys.** Independent release, independent scaling, hard blast-radius
limits, and an isolation story a regulator recognises.

**Costs.** The distribution premium in full: network failure modes,
distributed transactions, N backup stories, and contract tests as a
permanent tax. Uber (EV-0160) reached about 2,200 services and had to
reimpose domains, a five-layer call rule and per-domain gateways to
recover the discipline one deployable gives away.

### B. Module-shaped

**What it is.** Boundaries are logical and enforced in the build. One
process, one database, declared module interfaces, and a rule engine
that fails the build on a crossing.

**Buys.** Ordinary function calls, one transaction, one deploy, and
the split option kept open, because the module graph is the thing you
would split along. Shopify (EV-0159) is the large-scale existence
proof; Service Weaver (EV-0152) is the argued version, naming the
defect as conflating logical with physical boundaries.

**Costs.** No independent release. No hard isolation. Enforcement is
static, so dynamic wiring can cross a boundary while the check stays
green.

### C. Contract-shaped

**What it is.** The boundary that matters is the one you can
substitute or regenerate. A port with more than one plausible driver
or device, schema-first contracts, generated and committed clients
with a drift gate, vendor adapters owning the raw protocol.

**Buys.** Substitutability where substitution is actually real, and a
seam tests can drive without the runtime behind it.

**Costs.** Ceremony wherever no second device is plausible. Cockburn's
2005 pattern statement (EV-0150) never bounded this, which is where
the adapter-per-dependency habit comes from.

### D. Mixed, deliberately

**What it is.** B as the frame, C at the two or three seams that
genuinely substitute, A for the single component with a real volume or
regulatory asymmetry.

**Buys.** Each price paid only where the argument was made.

**Costs.** Needs a written record per seam, or it decays into
inconsistency nobody can explain later.

## Decision rule

Boundaries not yet proved stable under change, one release train, one
or two owners: **B**, and compose **C** at any seam with a real second
driver or device. A measured signal from DORA's list (EV-0151), a
change blocked on another owner, an inability to test in isolation, or
upstream-caused unplanned work: promote that one boundary to **A**,
one at a time, with the migration written. A regulatory or volume
asymmetry that exists today rather than in a roadmap: **A** for that
component only, from the start. Never **A** across the board because
of a label.

## Default

**B**, composed with **C**. Splitting is a response to a measurement,
never to an aesthetic.

## Worked rulings

- **Venture D (2026-06, argued)**: B, rings enforced by import-linter
  over a flat tree, later reaching for one database per service as a
  target once a second real owner existed.
- **Venture A (2026-07, argued)**: B with C at the vendor seams, and a
  constitutional carve-out for telemetry as the one volume-asymmetric
  component.
- **Venture B (2026, argued)**: B in substance, with one-way
  dependencies from app to api to engine. The erosion it suffered
  before the checks arrived is the reason WG-ARCH-001 binds.

## Counter-evidence

Service Weaver's co-location figures come from the authors' own
prototype with no independent replication. Fowler's monolith-first
position (EV-0153) is explicitly anecdotal and eleven years old. DORA
declines the framing entirely. EV-0010 is the reminder that
agent-era productivity intuitions have been measured wrong before.
Nothing here observed a one-person venture, so treat the rule as a
rule about enforcement, not a claim about scale.
