---
summary: Ignore rules alone, a pre-commit scan, a push-path scan, or a managed store with short-lived credentials?
type: guide
tags: [security, tooling, ci]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2027-04
sources: [EV-0034, EV-0037, EV-0220, EV-0221, EV-0222]
---

# GD-SEC-002: where does secret protection sit?

## The question

Credentials get into repositories by accident, and the accident is
cheap while the consequence is not: once history is pushed, rotation is
the only remedy and it is always late. The fork is where to put the
control, and every venture with a credential meets it on day one.

## It depends on

- Is the repository public, or public-adjacent through forks and CI
  logs? Push protection only exists on the hosting side.
- Who commits: a person, an agent, or both? Agents copy scaffolding
  files wholesale, which is exactly how example environment files leak.
- Can the platform issue short-lived credentials, or is a long-lived
  key the only option?
- What is the cost of a false block on a hot path, and who eats it?

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

## Default

B and C together, plus D wherever the platform supports it. Which
scanner is preference, not doctrine: gitleaks is declared feature
complete by its maintainer with security patches only and a named
successor, so that choice carries a review trigger (EV-0221).

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: B and C. The repository is
  documentation with no runtime credential, so D does not apply, and
  the binding requirement still stands because agent lanes commit here.
  The configured scan is a redacting history scan in CI plus a staged
  scan pre-commit.
- **PatterTech EOS (2026-08, argued)**: A rejected outright for any
  agent-writable repository. The deciding fact is EV-0220's statement
  that there is no built-in default deny list, which makes discipline
  the only control and agents have none.
- No venture ruling yet.

## Counter-evidence

Both sources for B and C are maintainer documentation rather than
studies (EV-0221, EV-0222), so the claim that two placements catch
more real leaks than one is reasoning, not measurement. We have no
controlled evidence for it and the pack says so. The SSDF outcome view
(EV-0037) supports the shape of the argument, that the outcome is what
binds and the tool is a choice, without evidencing the specific
placement pair. If someone runs the comparison, this default is the
first thing that should move.
