---
id: WG-ARCH-012
summary: Should a capability be built, bought as software or consumed as a managed service when exit and incident access are material?
kind: wargame
type: wargame
tags: [arch, eos, infra, money, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-ARCH-010, DOC-SUPPLY-009, DOC-SUPPLY-011]
gap_domain: capability-ownership
applies_when: [consumes_external_api, has_vendor_holding_identity_or_money, adds_dependency]
engages_when: [managed_service_changes_exit_or_access]
consequence: high
relations: [DREL-ARCH-002]
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0023, EV-0025, EV-0061, EV-0069, EV-0150, EV-0161, EV-0564]
review: 2027-08
lifecycle: active
---

# WG-ARCH-012: Who owns the capability?

## Decision question and stakes

Decide whether to build a capability, run bought or open software, or consume a
managed service when portability, evidence access and incident control matter.
The cheapest normal day can become the most expensive outage if the operator
cannot diagnose, export, restore or act without the provider.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-010` puts identity, money and handover-bound vendors behind an
  owned adapter with a written exit route.
- `DOC-SUPPLY-009` checks the release path for discontinuity at admission.
- `DOC-SUPPLY-011` reads a repository or delivery reality rather than trusting
  self-description.
- `DREL-ARCH-002` records that managed convenience depends on supply and exit
  evidence.
- The uncovered domain is `capability-ownership`.

## Preconditions and engagement triggers

Name the capability and consequence of loss. Record volume, latency,
compliance and support requirements, operator skill, build and run cost,
contract and price exposure, data and configuration export, audit evidence,
incident access, recovery objectives and the smallest viable alternative. For
identity or money, name the action that cannot wait for vendor support.

Applicability is any of `consumes_external_api`,
`has_vendor_holding_identity_or_money` or `adds_dependency`. Engage when
`managed_service_changes_exit_or_access` is true.

## Options

### A. Build and operate the minimum capability

Own source, runtime and recovery path, limiting scope to the differentiating
need. This gives maximum control and direct evidence. It also creates a product
and on-call obligation, and can underperform a mature service in security,
availability and specialist function.

### B. Run maintained third-party software

Adopt an inspectable package or product and own its deployment, data and
operations. This can preserve export and incident access while avoiding a
ground-up build. Upgrades, vulnerabilities, configuration and operational
expertise become the venture's responsibility.

### C. Managed service behind an owned adapter

Buy the capability but keep domain code, data mapping and provider calls behind
an owned seam. This reduces normal operations and keeps substitution possible.
The adapter cannot manufacture missing exports, evidence or provider-side
incident control.

### D. Managed service used directly

Adopt the provider's SDK, data model and workflow throughout because speed,
unique capability or ecosystem fit dominates. This minimises initial
translation and can expose the full product. It maximises coupling and makes a
provider outage, policy change or exit a broad product rewrite.

## Failure premises

### Premortem for A. Build and operate the minimum capability

Assume A failed. The team recreated commodity complexity, missed a security or
regulatory duty, and spent incident time learning a subsystem it could not
reliably operate.

### Premortem for B. Run maintained third-party software

Assume B failed. The project looked healthy but its actual release or security
path had changed, upgrades stalled, and the venture owned an operating burden
without owning the implementation direction.

### Premortem for C. Managed service behind an owned adapter

Assume C failed. The adapter covered API syntax but not identity, data,
workflow or incident semantics. During outage the provider supplied neither
the evidence nor the export needed to recover.

### Premortem for D. Managed service used directly

Assume D failed. Proprietary concepts spread through storage and interface
code, a price or policy change arrived before a migration path, and support
access was slower than the user harm.

## Decision rule

Choose C when the service meets the representative capability and proves
diagnosis, export and recovery, with the owned seam tested. Choose B when
control of data and incident operation is required and the venture can operate
the software. Choose A only for differentiating behaviour, a hard control
requirement unmet by candidates, or when operating the minimum is demonstrably
cheaper over the recorded horizon. Choose D only for reversible, low-consequence
capability or a unique service whose coupling and exit cost are explicitly
accepted.

For identity, money or irreplaceable records, no managed option passes without
a proved emergency action, complete export and restoration or replacement
route.

## Safe default

Use a maintained managed service behind the narrowest owned domain adapter,
provided the outage, export and restore exercise passes. Where a provider holds
identity, money or irreplaceable records and that proof is absent, there is no
safe default. The decision remains open or the scope is reduced.

## Cheapest discriminating test

Against the leading managed candidate, perform an outage drill, export all
venture-owned data and configuration, answer one incident question from the
available evidence, and restore or import the smallest useful journey into a
clean environment or credible substitute. Estimate the smallest owned
alternative using the same requirements.

## Fallback, exit and revisit

**Fallback `owned-minimum-seam`:** disable provider-unique features, retain the
owned domain record and route the minimum journey through the documented
manual or alternate path.

**Exit condition:** leave the option when required evidence, export, emergency
action, recovery objective or adapter boundary fails, or when contract or
release changes invalidate the accepted risk.

**Revisit trigger:** repeat on a price, terms, ownership, API, release,
incident-access or data-residency change, and before the provider takes custody
of a new consequential asset.

## Counter-evidence and transfer limits

An adapter improves substitution only for behaviour it actually contains.
Machine-readable contracts help define seams (EV-0023, EV-0025), but do not
prove a provider can export or recover. Repository health checks are heuristic
and measure hygiene, not product correctness (EV-0069). The ruling is bounded
to the named capability, consequence and evidence access. It does not make
`build` or `buy` an estate-wide preference.
