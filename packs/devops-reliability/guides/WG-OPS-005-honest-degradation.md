---
id: WG-OPS-005
summary: Should a service fail closed or preserve a reduced journey when availability conflicts with security, privacy or integrity floors?
kind: wargame
type: wargame
tags: [eos, ops, security, state, wargame]
scenario_modes: [conflict, exception, gap]
applicable_doctrines: [DOC-SUPPLY-003, DOC-DEVOPS-004, DOC-SEC-004, DOC-SEC-005, DOC-SEC-006, DOC-SUPPORT-001]
gap_domain: honest-service-degradation
applies_when: [deploys_to_environment, has_customer_visible_incident]
engages_when: [integrity_floor_reduces_availability]
consequence: high
relations: [DREL-OPS-001]
scope: estate
authority: advisory
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0020, EV-0041, EV-0220, EV-0225, EV-0578, EV-0581]
review: 2027-08
lifecycle: active
---

# WG-OPS-005: Fail closed or degrade honestly?

## Decision question and stakes

A dependency or control is unavailable. Decide whether the service must stop
the journey or can preserve a smaller useful outcome without weakening
privacy, authorisation, integrity, verification or approval. Availability is a
user outcome, but a fast incorrect, unauthorised or falsely verified result is
not service.

## Doctrines or coverage gap under pressure

- `DOC-SUPPLY-003` makes consuming-side verification fail closed.
- `DOC-SEC-004`, `DOC-SEC-005` and `DOC-SEC-006` protect secrets, personal
  data and consequential-action approval.
- `DOC-DEVOPS-004` requires a machine-readable user-facing objective.
- `DOC-SUPPORT-001` forbids reporting a bypassed check as passed.
- `DREL-OPS-001` records the tension between a protected integrity floor and
  availability.
- The uncovered domain is `honest-service-degradation`.

A Wargame cannot waive a binding floor. It can identify a reduced journey that
does not require the unavailable property.

## Preconditions and engagement triggers

Name the failing dependency, affected journey, protected properties, minimum
useful outcome, stale-data tolerance, permissible actions, customer message,
indicator, kill switch, owner and restoration criterion. Classify each action
as read, draft, queue, commit, authorise or external effect. State which claims
the reduced route can truthfully make.

Applicability is `deploys_to_environment` or
`has_customer_visible_incident`. Engage when
`integrity_floor_reduces_availability` is true.

## Options

### A. Fail the whole journey closed

Reject or pause the operation and expose a truthful unavailable state. This
protects every floor and is simplest to reason about. It can remove safe reads,
drafting or status work and turn one dependency failure into a total outage.

### B. Read-only or stale-but-labelled service

Serve a proved snapshot or cached result with age and limitations visible,
while blocking writes and consequential actions. This preserves orientation
and low-risk work. Staleness can still be harmful where status, permissions or
prices change quickly.

### C. Accept drafts or queue reversible intent

Let users prepare work or durably queue an intent without claiming acceptance
or finality. Process it after the protected dependency returns and revalidate
then. This preserves effort but can create duplicate, expired or conflicting
intent and requires a visible pending and cancellation model.

### D. Continue a reduced live write path

Permit only actions whose authorisation, integrity and compensation can be
proved without the failed component. This can retain a core journey but is the
highest-risk option because an apparently peripheral dependency may have been
the control enforcing a floor.

## Failure premises

### Premortem for A. Fail the whole journey closed

Assume A failed. Safe information and preparation were removed unnecessarily,
support load rose, and users adopted uncontrolled workarounds that created more
risk than a designed degraded route.

### Premortem for B. Read-only or stale-but-labelled service

Assume B failed. Staleness was hidden, cached authorisation outlived revocation,
or a user acted on obsolete state with a consequence the ruling had called
low-risk.

### Premortem for C. Accept drafts or queue reversible intent

Assume C failed. Pending work appeared committed, replay produced duplicates,
or the system applied an intent after its price, permission or context had
expired.

### Premortem for D. Continue a reduced live write path

Assume D failed. The route bypassed approval, verification or audit, and the
team discovered that compensation could not restore the protected property.

## Decision rule

If the unavailable component protects identity, authorisation, personal-data
purpose, integrity verification or consequential approval for the action,
select A for that action. Select B only when the snapshot age and content are
safe and visible. Select C when intent is reversible, idempotent, expires and
is revalidated before commitment. Select D only when every protected property
is enforced independently on the reduced path and a fault-injection test proves
it.

Degrade per journey and action, not per service label. A read route may remain
open while its write route fails closed.

## Safe default

Fail closed for protected writes and consequential actions. Preserve only
truthfully labelled read-only status or drafting that cannot be mistaken for a
completed action. There is no availability override for a binding security or
integrity floor.

## Cheapest discriminating test

Inject loss of the dependency during the representative journey. Verify the
promised minimum outcome, visible degraded state, SLI, alert, kill switch and
restoration. In the same run attempt an unauthorised, stale, duplicated and
unverified action and prove each remains blocked.

## Fallback, exit and revisit

**Fallback `protected-actions-closed`:** block every commit and external
effect, retain only a labelled status or draft route, and preserve queued work
without processing it.

**Exit condition:** disable degradation when a protected test fails, stale age
exceeds the ruling, queued intent cannot be cancelled or revalidated, or the
minimum journey cannot be distinguished from normal service.

**Revisit trigger:** repeat when a dependency, protected property, user
journey, cache policy, compensation path or restoration objective changes.

## Counter-evidence and transfer limits

Google describes graceful degradation as useful only when the rare path is
simple, exercised, monitored and switchable (EV-0581). That evidence is an
operational exemplar, not permission to spend privacy or integrity as an error
budget. Some low-risk journeys may benefit from broader degradation; some
safety or financial journeys may require full closure. A passing drill is
bounded to the injected dependency, journey, data age and protected-property
tests.
