---
id: WG-DEL-008
summary: What bounded delivery route mitigates an active incident when the normal gate is slower than the user harm?
kind: wargame
type: wargame
tags: [delivery, eos, ops, testing, wargame]
scenario_modes: [exception, gap]
applicable_doctrines: [DOC-DEL-001, DOC-DEL-004, DOC-SUPPLY-012, DOC-DEVOPS-008, DOC-SUPPORT-004]
gap_domain: incident-hotfix-gate
applies_when: [ships_code, has_customer_visible_incident]
engages_when: [incident_needs_gate_exception]
consequence: high
relations: [DREL-DEL-001]
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0026, EV-0204, EV-0209, EV-0423, EV-0563, EV-0580]
review: 2027-08
lifecycle: active
---

# WG-DEL-008: What is the incident hotfix gate?

## Decision question and stakes

An active incident is harming users and the normal delivery path is too slow.
Choose the smallest mitigation route that reduces current harm while retaining
known-good state, supervision, non-waivable checks, impact observation and a
tested rollback. A hotfix is a different gate with fewer, stronger checks. It
is never the absence of a gate.

## Doctrines or coverage gap under pressure

- `DOC-DEL-001` forbids weakening a check merely to make it pass.
- `DOC-DEL-004` requires every named gate to fail and to state threshold,
  scope and command.
- `DOC-SUPPLY-012` keeps one release path, including urgent releases.
- `DOC-DEVOPS-008` favours observed progressive rollout with automated abort.
- `DOC-SUPPORT-004` applies the pre-written severity ladder.
- `DREL-DEL-001` records how the urgent route supports, rather than bypasses,
  normal delivery control.
- The uncovered domain is `incident-hotfix-gate`.

Binding checks remain binding. If a mitigation requires changing their scope,
the protected review or ADR route applies despite the incident.

## Preconditions and engagement triggers

Declare incident severity, current user harm, incident commander or single
owner, live state record, last known-good version, affected journey, suspected
change, data migration state, rollback or kill switch, required approvals and
the smallest observation that proves harm is falling. Separate mitigation from
root-cause investigation.

Applicability is `ships_code` or `has_customer_visible_incident`. Engage when
`incident_needs_gate_exception` is true.

## Options

### A. Revert, disable or isolate

Return to a known-good artefact, disable the feature, shed the failing path or
isolate affected traffic. This usually changes the fewest assumptions and can
reduce harm quickly. It may be unsafe after an irreversible migration or when
the previous version carries the same fault.

### B. Configuration or data mitigation through a guarded runbook

Change a flag, limit, route or bounded record under explicit approval and
audit, then observe the affected journey. This can avoid a code build. It can
also create unreviewed persistent state or conceal the real fault if the
configuration path is not versioned and reversible.

### C. Minimal code patch through the emergency gate

Make one causal, reversible change, run the non-waivable checks plus the
smallest independent regression oracle, deploy to the smallest observable
slice and hold rollback ready. This addresses a defect directly but makes a
time-pressured diagnosis part of production risk.

### D. Continue the normal release gate

Use the full ordinary path because the harm is bounded, rollback is riskier or
the evidence is too weak for a safe emergency change. This protects assurance
but prolongs the incident if urgency was assessed correctly.

## Failure premises

### Premortem for A. Revert, disable or isolate

Assume A failed. Rollback met an incompatible schema, disabled a critical
journey without truthful status, or returned to a version that shared the
fault. The team confused a known version with known-good state.

### Premortem for B. Configuration or data mitigation through a guarded runbook

Assume B failed. An emergency value persisted beyond the incident, a manual
data change lacked an inverse, or the flag path had never been exercised and
created a second failure.

### Premortem for C. Minimal code patch through the emergency gate

Assume C failed. The diagnosis was wrong, the narrowed oracle missed a
neighbouring invariant, or rollout reached everyone before the impact signal
could abort it.

### Premortem for D. Continue the normal release gate

Assume D failed. The team optimised process compliance while preventable user
harm accumulated, and no one revisited the decision as impact increased.

## Decision rule

Choose A first when rollback, disablement or isolation is compatible with data
state and reduces the named harm. Choose B when the mitigation is pre-authorised,
audited, reversible and narrower than a code change. Choose C only when A and B
cannot settle the harm, the causal patch is smaller than the uncertainty it
removes, and non-waivable security, integrity, migration and independent
regression checks pass. Choose D when current harm is below the emergency
threshold or every emergency route increases expected harm.

Every option has one owner, one observation window and a rehearsed inverse.
No all-clear is issued until the impact signal, not merely deployment success,
shows recovery.

## Safe default

Use the ordinary release gate. Under proven emergency pressure, prefer the
smallest reversible mitigation in the order A, B, then C, each through the same
release identity with an emergency profile that preserves non-waivable checks.

## Cheapest discriminating test

Run a timed staging drill: declare the incident, apply the leading mitigation,
observe one user-journey signal, then roll it back. Seed a failing non-waivable
check and prove the emergency route blocks it. Record elapsed time, approvals,
artefact identity, known-good state, impact verdict and rollback result.

## Fallback, exit and revisit

**Fallback `known-good-or-safe-disable`:** restore the last version whose data
compatibility and journey were proved, or disable the affected capability with
a truthful status message.

**Exit condition:** abort the mitigation when the user-impact signal fails to
improve inside the recorded window, a non-waivable check fails, rollback is no
longer valid, or a protected property deteriorates.

**Revisit trigger:** reassess on each material incident-state change and after
the incident. Repeat the Wargame when deployment, schema, flag or rollback
machinery changes.

## Counter-evidence and transfer limits

Google's incident guidance places assessment and mitigation before root-cause
work, but its role structure assumes more responders than many EOS ventures
(EV-0580). Progressive delivery tooling can automate abort for serving metrics
but cannot reverse data already written (EV-0204). A feature flag is not
automatically safe and needs an owner, expiry and proved terminal path. A
successful drill proves the tested change and environment, not every emergency
release. The post-incident review restores full verification and removes every
temporary control.
