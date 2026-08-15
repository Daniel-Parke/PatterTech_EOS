---
id: GD-SUPPLY-003
summary: Floating ranges, continuous auto-merge, a cooldown window with batched moves, digest pins everywhere, or frozen?
kind: wargame
type: wargame
tags: [ci, delivery, eos, security, tooling, wargame]
scenario_modes: [selection, exception, conflict]
applicable_doctrines: [DOC-SUPPLY-005, DOC-DEVOPS-005, DOC-DEVOPS-008]
applies_when: [publishes_code]
engages_when: [dependency_update_changes_known_good]
consequence: high
relations: [DREL-SUPPLY-002]
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0038, EV-0069]
review: 2027-05
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SUPPLY-003: how far do we pin, and how often do we move?

## Decision question and stakes

Two failures sit at opposite ends of one dial. Move too fast and you
install a version that was malicious for four hours. Move too slowly and
you are running something with a known hole in it, and the upgrade you
eventually have to do spans two years of breaking changes. There is no
setting that avoids both, so the job is to pick a point deliberately and
write down which failure you accepted.

## Doctrines or coverage gap under pressure

- `DOC-SUPPLY-005` (default): A cooldown window before adopting a newly published version, with security fixes deliberately exempted.
- `DOC-DEVOPS-005` (binding): A restore drill runs on cadence and produces a dated evidence record with a measured elapsed time, a validation query and a result.
- `DOC-DEVOPS-008` (default): Progressive rollout with an automated abort condition for user-facing change.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How quickly does this ecosystem catch a compromised release, and does
  the registry allow a version to be replaced once published?
- Is there a test suite good enough that a green run means something?
- Who applies the update: a person, a bot, or an agent?
- Does the venture ship to somebody who cannot patch quickly afterwards?
- How many dependencies are there? The strategies scale differently.

Applicability is `publishes_code`. Engagement is `dependency_update_changes_known_good`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Floating ranges, resolved at build time
No lock file, or a lock file nobody commits. Buys nothing except
avoiding the work. Costs reproducibility outright: two builds of the
same commit produce different software, so a bisect is meaningless and
an incident cannot be reconstructed. It also means a malicious release
reaches you at the speed of your next build.

### B. Lock file, continuous bumps, auto-merge on green
A bot proposes every update and merges it when tests pass. Buys the
shortest exposure to known vulnerabilities and keeps upgrades small,
which is the real reason most teams that do this like it. Costs
exposure to the freshly published malicious version, because green tests
are not a malware check, and it hands the merge decision to a bot on the
day the ecosystem is under attack.

### C. Lock file, cooldown window, batched moves
The same bot, but nothing published inside a window of days is eligible,
and updates land in scheduled batches. Buys the head start: compromised
releases are typically found and pulled in hours, so a window measured
in days means the ecosystem usually finds them before you do. Costs
delayed patches, which the tooling makes visible rather than hiding: the
install keeps the vulnerable version, warns and exits non-zero. Security
fixes are normally exempted from the window, which is a deliberate hole
in the control and should be recognised as one.

### D. Digest pins everywhere, including transitive and toolchain
Every dependency, build step, base image and toolchain is named by
content digest, and moving anything is an explicit commit. Buys the
strongest reproducibility available without a hermetic build, and it is
the only option that covers the things a lock file misses: the container
base, the CI action, the compiler. Costs a great deal of mechanical
work unless a bot does the digest bumps for you, and it makes the diff
of an update unreadable to a human without tooling.

### E. Frozen
Pin and do not move except for a security fix. Buys stability and is
occasionally correct, for a released artefact under support that must
not change underneath its users. Costs an upgrade cliff that grows
until somebody has to take a month off to climb it, and it tends to be
chosen by accident rather than argued.

## Failure premises

### Premortem for A. Floating ranges, resolved at build time

Assume `A. Floating ranges, resolved at build time` was selected and the outcome failed. Test this option's stated failure mechanism first: reproducibility outright: two builds of the same commit produce different software, so a bisect is meaningless and an incident cannot be reconstructed. It also means a malicious release reaches you at the speed of your next build.

### Premortem for B. Lock file, continuous bumps, auto-merge on green

Assume `B. Lock file, continuous bumps, auto-merge on green` was selected and the outcome failed. Test this option's stated failure mechanism first: exposure to the freshly published malicious version, because green tests are not a malware check, and it hands the merge decision to a bot on the day the ecosystem is under attack.

### Premortem for C. Lock file, cooldown window, batched moves

Assume `C. Lock file, cooldown window, batched moves` was selected and the outcome failed. Test this option's stated failure mechanism first: delayed patches, which the tooling makes visible rather than hiding: the install keeps the vulnerable version, warns and exits non-zero. Security fixes are normally exempted from the window, which is a deliberate hole in the control and should be recognised as one.

### Premortem for D. Digest pins everywhere, including transitive and toolchain

Assume `D. Digest pins everywhere, including transitive and toolchain` was selected and the outcome failed. Test this option's stated failure mechanism first: a great deal of mechanical work unless a bot does the digest bumps for you, and it makes the diff of an update unreadable to a human without tooling.

### Premortem for E. Frozen

Assume `E. Frozen` was selected and the outcome failed. Test this option's stated failure mechanism first: an upgrade cliff that grows until somebody has to take a month off to climb it, and it tends to be chosen by accident rather than argued.

## Decision rule

- Every venture, floor: a committed lock file. A is not a strategy.
- Default: C plus D for the things a lock file does not cover. The
  cooldown goes on third-party dependencies; internal packages are
  exempted by name, which is what the exclusion list is for.
- B where the venture ships to somebody who cannot patch quickly and
  known vulnerabilities are the dominant risk, and then only with the
  cooldown kept for the highest-fanout dependencies.
- E for a released artefact under support, with a written end date for
  the freeze. A freeze with no end date is a decision to have a crisis
  later.
- Whatever the cadence, read the repository before depending on it
  rather than reading its self-description (EV-0069), and verify what
  arrives at admission rather than trusting the workflow that produced
  it (EV-0038).
- Never one cooldown policy across ecosystems. Where tags are mutable,
  re-pushing an existing tag restarts the clock, so the same policy
  that works for a package registry does nothing for a container
  registry unless you pin by digest.

## Safe default

C, with D for base images, build steps and toolchains, security fixes
exempt from the window, and the exemption list short and argued.

## Cheapest discriminating test

Take one representative security update through the cooldown exception, suite, staged release, rollback and incident reconstruction path. Compare that proof with the known-good deployment it would replace.

## Fallback, exit and revisit

**Fallback `safe-default`:** C, with D for base images, build steps and toolchains, security fixes exempt from the window, and the exemption list short and argued.

**Exit condition:** Stop or roll back the selected branch when reproducibility outright: two builds of the same commit produce different software, so a bisect is meaningless and an incident cannot be reconstructed. It also means a malicious release reaches you at the speed of your next build, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How quickly does this ecosystem catch a compromised release, and does the registry allow a version to be replaced once published?

## Counter-evidence and transfer limits

The cooldown case rests on incident timelines and maintainer
documentation, not on a controlled comparison. Reported detection times
for the compromises that motivated the feature are a few hours, and the
commonly suggested window is a week, which is roughly two orders of
magnitude of margin chosen by feel. Nobody has measured how many real
compromises a one-day window would have caught against a seven-day one.

The tooling's own documentation states the limit that matters: a
cooldown does nothing about ordinary vulnerabilities in code that was
never malicious, and it delays their fixes. A venture whose real risk is
unpatched known holes rather than active compromise should read this
guide the other way round and choose B.

The exemption for security updates is a judgement made by whichever tool
classifies them, not a fact about the update. A malicious release
published as a security fix is exactly the shape that exemption lets
through.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
