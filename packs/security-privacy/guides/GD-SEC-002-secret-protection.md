---
id: GD-SEC-002
summary: Ignore rules alone, a pre-commit scan, a push-path scan, or a managed store with short-lived credentials?
kind: wargame
type: wargame
tags: [ci, eos, security, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-SEC-018]
applies_when: [runs_agents]
engages_when: [operator_requests_wargame]
consequence: high
relations: []
always_walk: true
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0034, EV-0037, EV-0220, EV-0221, EV-0222]
review: 2027-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SEC-002: where does secret protection sit?

## Decision question and stakes

Credentials get into repositories by accident, and the accident is
cheap while the consequence is not: once history is pushed, rotation is
the only remedy and it is always late. The fork is where to put the
control, and every venture with a credential meets it on day one.

## Doctrines or coverage gap under pressure

- `DOC-SEC-018` (default): Configured secret scan: a redacting history scan in CI and a staged scan pre-commit.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is the repository public, or public-adjacent through forks and CI
  logs? Push protection only exists on the hosting side.
- Who commits: a person, an agent, or both? Agents copy scaffolding
  files wholesale, which is exactly how example environment files leak.
- Can the platform issue short-lived credentials, or is a long-lived
  key the only option?
- What is the cost of a false block on a hot path, and who eats it?

Applicability is `runs_agents`. Engagement is `operator_requests_wargame`. This is an always-walk decision.

## Options

### A. Ignore rules and discipline
A gitignore entry and a team habit. Buys nothing to install and no
false positives. Costs everything on the first mistake, because the
control is a memory of a rule rather than a check. Agents have no such
memory and there is no useful built-in deny list, so unnamed means
unprotected (EV-0220).

### B. Pre-commit scan on the developer machine
A staged-content scan before the commit is written. Buys the earliest
possible catch, before anything enters history, and it is fast because
it looks at a diff. Costs a local install and it is bypassable by
design: any developer or agent can skip the hook, and a hook that
cannot be skipped becomes a hook people uninstall (EV-0221).

### C. Push-path scan on the hosting side
The host refuses the push when it detects a supported pattern
(EV-0222). Buys a control nobody can skip locally and one that covers
every client. Costs coverage limits: it detects the patterns it knows,
so a bespoke credential format passes, and it fires after the secret is
already in local history, so the remedy is a rewrite rather than an
amend.

### D. Managed store plus short-lived credentials
The secret never exists as a file: the runtime fetches it, or the
platform issues a token that expires. Buys removal of the precondition
rather than detection of the symptom, and it shrinks the blast radius
of any leak that still happens. Costs platform support, setup time, and
a new failure mode when the store is unreachable.

## Failure premises

### Premortem for A. Ignore rules and discipline

Assume `A. Ignore rules and discipline` was selected and the outcome failed. Test this option's stated failure mechanism first: everything on the first mistake, because the control is a memory of a rule rather than a check. Agents have no such memory and there is no useful built-in deny list, so unnamed means unprotected (EV-0220).

### Premortem for B. Pre-commit scan on the developer machine

Assume `B. Pre-commit scan on the developer machine` was selected and the outcome failed. Test this option's stated failure mechanism first: a local install and it is bypassable by design: any developer or agent can skip the hook, and a hook that cannot be skipped becomes a hook people uninstall (EV-0221).

### Premortem for C. Push-path scan on the hosting side

Assume `C. Push-path scan on the hosting side` was selected and the outcome failed. Test this option's stated failure mechanism first: coverage limits: it detects the patterns it knows, so a bespoke credential format passes, and it fires after the secret is already in local history, so the remedy is a rewrite rather than an amend.

### Premortem for D. Managed store plus short-lived credentials

Assume `D. Managed store plus short-lived credentials` was selected and the outcome failed. Test this option's stated failure mechanism first: platform support, setup time, and a new failure mode when the store is unreachable.

## Decision rule

- Any repository with a credential, always: B and C together. They fail
  differently, which is the whole argument for both. Name the
  credential files and secret environment variables explicitly in the
  deny list, because the default list protects nothing (EV-0220).
- Agents commit in this repository: B and C are not optional and a
  bypass must record a stated reason and leave an audit record.
- The platform can issue short-lived credentials: D as well, and drop
  the long-lived key entirely rather than keeping it as a fallback.
- The repository is private, single-operator, and holds no credential
  at all: A is honest, and the pack's `holds_credentials` predicate is
  false, so this guide does not apply.
- Never C alone on a repository where agents copy scaffolding. The
  example environment file is the classic carrier and it usually
  carries a pattern the host does not recognise.

## Safe default

B and C together, plus D wherever the platform supports it. Which
scanner is preference, not doctrine: gitleaks is declared feature
complete by its maintainer with security patches only and a named
successor, so that choice carries a review trigger (EV-0221).

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is the repository public, or public-adjacent through forks and CI logs? Push protection only exists on the hosting side.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B and C together, plus D wherever the platform supports it. Which scanner is preference, not doctrine: gitleaks is declared feature complete by its maintainer with security patches only and a named successor, so that choice carries a review trigger (EV-0221).

**Exit condition:** Stop or roll back the selected branch when everything on the first mistake, because the control is a memory of a rule rather than a check. Agents have no such memory and there is no useful built-in deny list, so unnamed means unprotected (EV-0220), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is the repository public, or public-adjacent through forks and CI logs? Push protection only exists on the hosting side.

## Counter-evidence and transfer limits

Both sources for B and C are maintainer documentation rather than
studies (EV-0221, EV-0222), so the claim that two placements catch
more real leaks than one is reasoning, not measurement. We have no
controlled evidence for it and the pack says so. The SSDF outcome view
(EV-0037) supports the shape of the argument, that the outcome is what
binds and the tool is a choice, without evidencing the specific
placement pair. If someone runs the comparison, this default is the
first thing that should move.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
