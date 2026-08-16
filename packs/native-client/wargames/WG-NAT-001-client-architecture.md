---
id: WG-NAT-001
summary: Which client architecture does this product take?
kind: wargame
type: wargame
tags: [a11y, arch, delivery, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-NAT-008]
applies_when: [ships_a_binary]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0171, EV-0230, EV-0372, EV-0384, EV-0385, EV-0386, EV-0387]
review: 2028-05
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-NAT-001: Which client architecture does this product take?

## Decision question and stakes

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

## Doctrines or coverage gap under pressure

- `DOC-NAT-008` (default): Shared logic with a native user interface.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `ships_a_binary`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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
web-team reuse and the over-the-air path in WG-NAT-003. Costs standing
upgrade work and third-party native module readiness you cannot see in
advance.

**Not an option: the wrapped website.** A repackaged site is rejected
outright under review rule 4.2 (EV-0372).

## Failure premises

### Premortem for A. Two native codebases

Assume `A. Two native codebases` was selected and the outcome failed. Test this option's stated failure mechanism first: two of everything, including two accessibility passes and two release trains.

### Premortem for B. Shared logic, native user interface

Assume `B. Shared logic, native user interface` was selected and the outcome failed. Test this option's stated failure mechanism first: a build seam, and a toolchain fewer people know.

### Premortem for C. Own the renderer

Assume `C. Own the renderer` was selected and the outcome failed. Test this option's stated failure mechanism first: platform conventions, accessibility services and system controls, which arrive only as far as the framework has reimplemented them, and the repository publishes no per-target maturity grade.

### Premortem for D. Platform widgets driven by shared code

Assume `D. Platform widgets driven by shared code` was selected and the outcome failed. Test this option's stated failure mechanism first: model rather than as a criticism: the seam between shared and platform code is a permanent migration surface the team inherits. On a zero-major version scheme, semantic versioning expectations (EV-0171) do not apply and every upgrade is potentially breaking. Buys web-team reuse and the over-the-air path in WG-NAT-003. Costs standing upgrade work and third-party native module readiness you cannot see in advance.

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

## Safe default

B, shared logic with a native user interface. It takes the decision
that is graded Stable and declines the one that is not, and it keeps
the accessibility and platform-behaviour properties that cost the most
to rebuild.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Team shape.** Whether the people writing the client are the people writing the web product, and whether anyone on the team has shipped on both platforms.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B, shared logic with a native user interface. It takes the decision that is graded Stable and declines the one that is not, and it keeps the accessibility and platform-behaviour properties that cost the most to rebuild.

**Exit condition:** Stop or roll back the selected branch when two of everything, including two accessibility passes and two release trains, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Team shape.** Whether the people writing the client are the people writing the web product, and whether anyone on the team has shipped on both platforms.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Team shape.** Whether the people writing the client are the people writing the web product, and whether anyone on the team has shipped on both platforms.** and ****Where the risk actually is.** Business-rule divergence between platforms is a different problem from interface cost, and different architectures solve different ones.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
