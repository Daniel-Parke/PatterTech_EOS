---
summary: Flag registry fields, expiry and terminal value, and the rollout object's failure condition and abort
type: implementation
tags: [ops, delivery, infra]
kind: recipe
scope: estate
review: 2028-03
sources: [EV-0026, EV-0059, EV-0204, EV-0209]
---

# Flag and rollout lifecycle

Level-3 reference for binding requirement 7 and for
`packs/devops-reliability/wargames/WG-DEVOPS-002-release-control.md`.

## Why a flag needs an expiry at creation

Stale flag cleanup is a mechanical refactoring problem: when a flag
reaches its terminal state, a tool can rewrite the syntax tree, delete
the dead branch and raise the change automatically (EV-0209). That only
works if the flag declared an expiry and a terminal value up front,
because otherwise the automation has nothing to act on. A small codebase
gets most of the value from a scheduled report of flags past expiry
rather than from automated rewriting, but the field is the same field.

The flag evaluation standard itself standardises the interface and not
the lifecycle, and stale-flag debt is a known failure mode it does not
address (EV-0026). Lifecycle is ours to carry.

## Flag registry fields

Every entry, no exceptions:

```yaml
flags:
  - key: contacts_read_path
    owner: daniel
    created: 2026-08-03
    expires: 2026-10-01
    terminal_value: true
    purpose: read email addresses from contacts instead of users.email_address
    kind: release
```

- `owner` is a person, never a team alias that resolves to nobody.
- `expires` is a date in the future at creation. A flag past its expiry
  is a finding, not a reminder.
- `terminal_value` is what the flag will be when the branch is deleted.
  Writing it at creation forces the question of what the flag is for.
- `kind` is `release`, `experiment`, `ops` or `permission`. Only
  `permission` flags are permitted to be permanent, and they still carry
  an owner and a review date.

## Experiment flags

Experiment flags decide on asymmetric gating: goal metrics drive the
ship decision, guardrail metrics block only on statistically significant
harm, and a recommendation fires once a pre-declared precision target is
reached (EV-0059). That source is vendor documentation of its own
feature, so the defaults it publishes are conventions rather than
validated optima. The structure is worth copying; the numbers are not.

## The rollout object

A progressive rollout is a machine decision against a declared query
(EV-0204). The object names four things:

1. The metric provider and the query.
2. A success condition.
3. A failure condition.
4. A failure limit that tolerates transient noise.

Breaching the failure limit aborts the rollout and shifts traffic back
to the last stable version automatically, so the rollback path lives in
the deployment object rather than in a runbook. The declared query is
also what makes the promotion auditable after the fact.

```yaml
analysis:
  metric: error-rate
  provider: prometheus
  interval: 1m
  successCondition: result < 0.01
  failureCondition: result >= 0.05
  failureLimit: 2
  onFailure: abort
```

A rollout configuration with no failure condition is not progressive
delivery; it is a slow deploy.

## The hole neither half closes

Automatic abort protects the serving tier. It does not unwrite rows the
canary already wrote (EV-0204). Any change that writes under the new
path must be compatible with the old reader for the whole rollout, which
puts the change back inside the expand, migrate, contract discipline in
`packs/devops-reliability/wargames/WG-DEVOPS-001-schema-change-strategy.md`.
Treating an abort as a rollback for data is the mistake this section
exists to prevent.

## Removal

Removal is work, scheduled at creation by the expiry date. The order is:
set the flag to its terminal value everywhere, confirm no evaluation of
the other branch for a full window, delete the branch, delete the
registry entry. Deleting the registry entry first leaves an orphaned
branch nobody can find.
