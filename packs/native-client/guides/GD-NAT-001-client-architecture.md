---
summary: Which client architecture does this product take?
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0171, EV-0230, EV-0372, EV-0384, EV-0385, EV-0386, EV-0387]
review: 2028-05
type: guide
tags: [arch, delivery, a11y]
---

# GD-NAT-001: Which client architecture does this product take?

## The question

Four architectures are in serious use, and the choice sets the cost of
every later decision: how many accessibility passes, how many release
trains, how much platform behaviour arrives for free, and what has to
be migrated when a framework moves. It is close to irreversible once a
product ships.

The honest starting point: there is no measured answer. We could not
obtain a retrievable, methodologically serious comparison of these
architectures on performance, energy or defect rate. Treat every
framework performance claim as unevidenced, and decide on the things
that are documented.

## It depends on

- **Team shape.** Whether the people writing the client are the people
  writing the web product, and whether anyone on the team has shipped
  on both platforms.
- **Where the risk actually is.** Business-rule divergence between
  platforms is a different problem from interface cost, and different
  architectures solve different ones.
- **How much the product competes on platform feel.** A tool people
  live in all day is judged against its neighbours on the home screen.
- **Accessibility obligation.** Platform semantics APIs are richest
  where you use the platform's own toolkit (EV-0387).
- **Whether one platform carries the revenue.** Two codebases for a
  product with a ninety-ten split is two release trains for a tenth of
  the money.

## Options

### A. Two native codebases
SwiftUI and Compose, written separately. Platform conventions,
accessibility services and system controls arrive with the toolkit,
which is what the platform guidance assumes (EV-0230), and the
semantics APIs are richest here (EV-0387). Buys the best
platform behaviour and the smallest framework risk. Costs two of
everything, including two accessibility passes and two release trains.

### B. Shared logic, native user interface
Kotlin Multiplatform, or a Rust core with native shells. The vendor
grades this honestly and per target: the core is Stable on Android,
iOS, JVM and JS, while the shared interface layer carries a separate
and independent grade (EV-0386). Buys one implementation of the
domain rules with platform behaviour intact. Costs a build seam, and
a toolchain fewer people know.

### C. Own the renderer
Flutter. The framework draws everything itself and compiles to machine
code per platform, so behaviour is identical everywhere
(EV-0385). Buys one surface and one team. Costs platform
conventions, accessibility services and system controls, which arrive
only as far as the framework has reimplemented them, and the repository
publishes no per-target maturity grade.

### D. Platform widgets driven by shared code
React Native. The project rewrote its own interop layer, defaulting to
the new one from 0.76 after opt-in from 0.68, and still ships an
opt-out without declaring the old path dead (EV-0384). Read that
as the cost model rather than as a criticism: the seam between shared
and platform code is a permanent migration surface the team inherits.
On a zero-major version scheme, semantic versioning expectations
(EV-0171) do not apply and every upgrade is potentially breaking. Buys
web-team reuse and the over-the-air path in GD-NAT-003. Costs standing
upgrade work and third-party native module readiness you cannot see in
advance.

**Not an option: the wrapped website.** A repackaged site is rejected
outright under review rule 4.2 (EV-0372).

## Decision rule

If one platform carries the revenue and the surface is small and deep,
take A for that platform alone. If the product's main risk is business
rules drifting between platforms, take B. If a brand-uniform,
deliberately non-native design language across many targets is the
point, take C, and budget the accessibility work you have just stopped
inheriting. If the client team and the web team are the same people, or
an existing JavaScript product needs a client quickly and the
over-the-air path is worth real money, take D.

Never decide on a published performance comparison. None that we could
retrieve is serious.

## Default

B, shared logic with a native user interface. It takes the decision
that is graded Stable and declines the one that is not, and it keeps
the accessibility and platform-behaviour properties that cost the most
to rebuild.

## Worked rulings

- **native-client pack exemplar (2026-08, argued)**: B, on a two-person
  team with one booking invariant that must behave identically on both
  platforms and a screen count in single figures. Runner-up was A,
  refused on release-train cost. See
  `packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md`.
- **Grading as disclosure (external, inherited)**: the per-target
  stability grade (EV-0386) is what makes a cross-platform bet
  auditable. Neither C nor D publishes a comparable grade, and the
  absence is evidence of less disclosure, not of lower maturity.
