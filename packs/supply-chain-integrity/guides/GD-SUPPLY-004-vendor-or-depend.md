---
id: GD-SUPPLY-004
summary: Depend with a pin, vendor the source, fork and maintain, reimplement the slice you need, or use the platform?
kind: wargame
type: wargame
tags: [arch, delivery, eos, security, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-SUPPLY-011]
applies_when: [publishes_code]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0069]
review: on-change-of:EV-0069
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SUPPLY-004: do we vendor it or depend on it?

## Decision question and stakes

You need a piece of somebody else's code. It can stay theirs and arrive
through a resolver, or it can become yours and sit in the tree. The
question gets asked as a build-reliability question and answered as one,
which is how a team ends up owning a copy of a library nobody reads,
receiving none of its security fixes, and calling that supply chain
hardening.

Licence obligations that follow the copy are `legal-licensing`'s
question, not this one. Cross-link and go there before choosing B or C.

## Doctrines or coverage gap under pressure

- `DOC-SUPPLY-011` (default): Read the repository, not its self-description, before depending on it.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is the dependency small enough that a person could actually read it?
- How often does it change, and do those changes matter to you?
- Can your build reach the registry at build time, in every environment
  including the one with no network?
- Is the concern integrity, availability, or the maintainer's future?
  Those want different answers.
- Who is going to read the diff on every update, by name?

Applicability is `publishes_code`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Depend, pinned
Named in the manifest, pinned by digest in the lock file, updated by a
bot on a cadence. Buys upstream's fixes automatically, keeps the diff
small, keeps the tree readable. Costs a build-time dependency on the
registry, and it means a compromised release upstream reaches you on
whatever schedule GD-SUPPLY-003 set.

### B. Vendor the source into the tree
Copy it in, build from the copy. Buys builds that work offline, exact
knowledge of what is being compiled, and a diff on every update that a
person can review. Costs the fixes: nothing arrives unless somebody
pulls it. And there is a trap in the mechanics worth knowing: at least
one major toolchain stops verifying hashes once a vendor directory is in
use, checking only that the vendored manifest agrees with the module
file. Vendoring moves verification from the resolver to the moment the
directory was generated, and from there to whoever reads the diff. If
nobody reads it, verification has moved to nowhere.

### C. Fork and maintain
Take ownership, carry your own changes, merge upstream when you choose.
Buys the ability to fix things upstream will not. Costs a permanent
maintenance line on your own team, and the cost compounds: every
upstream release is now a merge. Correct when upstream is unresponsive
and the code is load-bearing, and a slow disaster the rest of the time.

### D. Reimplement the slice you need
Write the twenty lines you actually use. Buys zero dependency, zero
licence question, and code your team understands. Costs your own bugs
in a problem somebody else already solved, and the cost is worst
exactly where it looks cheapest: date handling, character encoding,
retries, anything with edge cases you have not met yet.

### E. Use the platform or the standard library
Check whether the runtime already does it. Buys a dependency that ships
with the thing you already trust. Costs capability, usually, because the
standard library version is more basic. Chronically under-considered,
because reaching for a package is faster than reading the manual.

## Failure premises

### Premortem for A. Depend, pinned

Assume `A. Depend, pinned` was selected and the outcome failed. Test this option's stated failure mechanism first: a build-time dependency on the registry, and it means a compromised release upstream reaches you on whatever schedule GD-SUPPLY-003 set.

### Premortem for B. Vendor the source into the tree

Assume `B. Vendor the source into the tree` was selected and the outcome failed. Test this option's stated failure mechanism first: the fixes: nothing arrives unless somebody pulls it. And there is a trap in the mechanics worth knowing: at least one major toolchain stops verifying hashes once a vendor directory is in use, checking only that the vendored manifest agrees with the module file. Vendoring moves verification from the resolver to the moment the directory was generated, and from there to whoever reads the diff. If nobody reads it, verification has moved to nowhere.

### Premortem for C. Fork and maintain

Assume `C. Fork and maintain` was selected and the outcome failed. Test this option's stated failure mechanism first: a permanent maintenance line on your own team, and the cost compounds: every upstream release is now a merge. Correct when upstream is unresponsive and the code is load-bearing, and a slow disaster the rest of the time.

### Premortem for D. Reimplement the slice you need

Assume `D. Reimplement the slice you need` was selected and the outcome failed. Test this option's stated failure mechanism first: your own bugs in a problem somebody else already solved, and the cost is worst exactly where it looks cheapest: date handling, character encoding, retries, anything with edge cases you have not met yet.

### Premortem for E. Use the platform or the standard library

Assume `E. Use the platform or the standard library` was selected and the outcome failed. Test this option's stated failure mechanism first: capability, usually, because the standard library version is more basic. Chronically under-considered, because reaching for a package is faster than reading the manual.

## Decision rule

- Default A. It is the option where security fixes arrive without
  anybody remembering to fetch them, which over a year is worth more
  than any of the others buy.
- E first for anything small. Check the runtime before adding a name to
  the manifest.
- D when the slice you use is genuinely small, well specified, and not
  in a category famous for edge cases. Write the test that proves you
  match, not just the code.
- B for a named reason: an air-gapped build, a dependency that has gone
  unmaintained, or a build that must not reach the network. Name the
  person who reads the diff on every update, and check that the toolchain
  still verifies what you think it verifies.
- C only when upstream is unresponsive, the code is load-bearing, and
  somebody has agreed to own it. Put an end condition on it: either
  upstream revives and you go back to A, or the fork becomes the
  product.
- Before A or B, read the repository rather than its self-description
  (EV-0069): who can publish, whether releases are automated, whether
  anything has been released recently at all.

## Safe default

A, pinned. B only with a named reason and a named reader.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is the dependency small enough that a person could actually read it?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, pinned. B only with a named reason and a named reader.

**Exit condition:** Stop or roll back the selected branch when a build-time dependency on the registry, and it means a compromised release upstream reaches you on whatever schedule GD-SUPPLY-003 set, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is the dependency small enough that a person could actually read it?

## Counter-evidence and transfer limits

The strongest case against A is the one this whole pack is about: a
pinned dependency still executes somebody else's code on your build
machine, and a compromised release reaches you when you next move. B
genuinely removes that, for as long as you do not move.

The strongest case against B is not the maintenance cost, which people
expect, but the silence. A vendored tree produces no bot pull request,
no advisory notification and no version number in a report, so nobody is
reminded it exists. That is why the decision rule names a person rather
than a process: a process for reading vendored diffs is exactly the kind
of thing that stops happening without anybody noticing.

There is no measurement here. This guide rests on toolchain
documentation and on the shape of the failure, not on a study comparing
vendoring against depending, and work that leans on it should say so.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
