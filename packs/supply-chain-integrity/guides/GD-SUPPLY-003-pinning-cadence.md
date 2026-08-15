---
summary: Floating ranges, continuous auto-merge, a cooldown window with batched moves, digest pins everywhere, or frozen?
type: guide
tags: [security, delivery, ci, tooling]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2027-05
sources: [EV-0038, EV-0069]
---

# GD-SUPPLY-003: how far do we pin, and how often do we move?

## The question

Two failures sit at opposite ends of one dial. Move too fast and you
install a version that was malicious for four hours. Move too slowly and
you are running something with a known hole in it, and the upgrade you
eventually have to do spans two years of breaking changes. There is no
setting that avoids both, so the job is to pick a point deliberately and
write down which failure you accepted.

## It depends on

- How quickly does this ecosystem catch a compromised release, and does
  the registry allow a version to be replaced once published?
- Is there a test suite good enough that a green run means something?
- Who applies the update: a person, a bot, or an agent?
- Does the venture ship to somebody who cannot patch quickly afterwards?
- How many dependencies are there? The strategies scale differently.

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

## Default

C, with D for base images, build steps and toolchains, security fixes
exempt from the window, and the exemption list short and argued.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: the lock file is the control
  here, and until 2026-08-15 it was single-platform, which is the
  defect class this capability owns and is recorded in the coverage
  row. No cooldown is configured, because the dependency set is a
  handful of Python tools; the honest position is that this repository
  is at the floor and not at the default.
- No venture ruling yet.

## Counter-evidence

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
