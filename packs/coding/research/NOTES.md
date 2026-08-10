---
summary: Research synthesis for the coding pack, four construction philosophies, review at scale, and what should bind
type: example
tags: [eos]
---

# Coding pack research notes

Cutoff 2026-08-03. Twenty new sources in `sources.fragment.json`, plus
existing ledger records cited by EV id. The domain question is not
"what is good code". It is: when an agent writes most of the code, what
survives from human construction practice, and what has to be rebuilt.

## Four construction philosophies, and when each fits

These are materially different, not flavours of one thing. They differ
in where the oracle comes from, and that is the axis that matters when
the author is a model.

**1. Test-first, oracle-first.** Write the executable statement of
intent before the code. Evidence for humans is weaker than the folklore
claims: FRAG-CODING-15 dissected the process across 39 professionals
and found quality and productivity tracked granularity and uniformity,
not sequencing. Test-first is a work-decomposition discipline wearing a
ritual. For agents the picture inverts. EV-0007 found generating tests
after faulty code roughly halves fault detection, EV-0003 cut
regressions from 6.08 to 1.82 per cent with targeted test-impact
analysis, EV-0004 reached 94.3 per cent on SWE-bench Verified when
human-written tests were supplied. The mechanism differs: for a human
the test is a design aid, for a model it is the only reliable oracle.
Fits: anything with a stateable acceptance condition, any FIX, any
change to a boundary. Anti-pattern: EV-0006 found agents mostly write
observational prints they then discard, so "the agent wrote tests" is
not evidence that tests exist.

**2. Grow the system incrementally, change-driven.** Refactor when a
pending change demands it. FRAG-CODING-14 surveyed contributors about
specific detected refactorings and found motivation is overwhelmingly
situational, not smell-driven. That kills the smell-detector backlog as
a model of the work. For code you did not write, the entry move is
characterisation: FRAG-CODING-17 shows approval testing gets a
behaviour net around opaque code in minutes by inverting the assertion.
Fits: inherited code, agent-written code you are about to change,
anything where the specification is lost. Anti-pattern: treating
approved files as a specification. They lock in current bugs, and
approvals become reflexive rubber stamps, which is exactly the
low-confidence test volume EV-0094 warns about.

**3. Contract-first.** Declare the interface, then let implementations
race to satisfy it. Already well covered in the ledger: EV-0023
(OpenAPI), EV-0024 (AsyncAPI), EV-0025 (JSON Schema), EV-0057 (dbt
model contracts, freeze only the interface), EV-0011 (MCP, version the
contract by date). FRAG-CODING-12 extends it to a place teams usually
miss: wrapping an error makes that error part of your API, so the set
of distinguishable failure modes is contract surface and must be
declared and versioned like any other. FRAG-CODING-08 supplies the
versioning grammar and the precondition everyone skips, that the public
API must be declared precisely before the numbers mean anything. Fits:
any boundary crossed by two agents, two ventures or two release trains.
Anti-pattern: contract ceremony on internals, where it buys rigidity
and no coordination.

**4. Generate and gate.** Let the model write broadly, put the quality
bar downstream in machine checks. FRAG-CODING-18 is the reason this is
not optional: roughly 40 per cent of generated programs in CWE-relevant
scenarios were vulnerable, and the rate varied with prompt and domain
in ways the author cannot see. EV-0070 (Semgrep, diff-aware policy as
executable rules) and EV-0069 (Scorecard) are the shape of the gate.
EV-0008 (Agentless) is the sober counterweight: a fixed
localise-repair-validate pipeline matched autonomous agents at lower
cost, so gating plus a dumb pipeline often beats sophistication. Fits:
high-volume mechanical change. Anti-pattern: gates that only run on the
whole repo, which produces alert fatigue and gets disabled.

## Code review at scale

FRAG-CODING-01 (Google eng-practices) gives the only review rule worth
making binding: approve once the change definitely improves overall
code health even when imperfect, refuse only what definitely worsens
it, and settle style by the style guide rather than by taste. Note the
repository was archived read-only on 2025-11-21, so it is a fixed
historical artefact, not living guidance.

FRAG-CODING-02 describes what that produces at scale: mostly small,
single-reviewer changes, around 70 per cent committed under 24 hours,
over 80 per cent with at most one iteration. FRAG-CODING-03, at a
different company, found the defect-finding expectation largely unmet
and most value arriving as knowledge transfer and awareness, with
reviewer understanding as the binding constraint.

That is the load-bearing tension for us. If review's real product is
knowledge transfer between humans, a solo operator directing agents
gets almost none of it, and mandatory human review is ceremony.
FRAG-CODING-04 states that argument explicitly and concludes for
agent-led review with human oversight reserved for high-risk changes.
It is a preprint with no new data, so treat it as a hypothesis. Its
concessions are the usable part: hallucinated approvals, unsolved
prompt injection, weak architectural judgement, and an accountability
gap when an auto-approved change causes harm.

## Flow, history and repository shape

FRAG-CODING-05 (DORA, CC BY 4.0) gives trunk-based development four
measurable conditions rather than an ideology: three or fewer active
branches, branch lifetime in hours, at least one merge to trunk per day,
no code freezes. FRAG-CODING-20 adds the ladder (direct commit, then
short-lived branches, then merge queue) and names feature flags and
branch by abstraction as the mechanisms that make big changes
compatible with continuous merging. Both are association or opinion,
not causal evidence, and the site is stale.

FRAG-CODING-07 (Conventional Commits) is worth adopting only if
something downstream consumes it. As decoration it is pure ceremony.
With agent authors the spec's own escape hatch matters: normalise at
merge rather than expecting every commit to comply.

Monorepo versus polyrepo has no winner. FRAG-CODING-09 reports the
benefits at two billion lines and is candid that they are bought with
bespoke tooling most organisations cannot fund. FRAG-CODING-10
catalogues the countervailing costs. The honest reading for a venture
estate is that small repos get monorepo benefits free because they are
small, and the pain is in the middle.

## Disagreements worth recording

- **Sequencing.** FRAG-CODING-15 says test-first is not the active
  ingredient for humans. EV-0003, EV-0004, EV-0005 and EV-0007 say it
  is decisive for agents. Not a contradiction once you see the
  mechanism differs, but it means human TDD literature must not be
  cited as evidence for agent practice or the reverse.
- **Is AI degrading codebases.** FRAG-CODING-16 reports refactoring
  moves down about 70 per cent, duplication up about 81 per cent and
  error-masking constructs up about 47 per cent across 623 million
  changes. It is vendor-run, non-random, method behind a form, causal
  attribution by timing. FRAG-CODING-06 (DORA 2025) finds delivery
  outcomes flat, not worse. EV-0010 (METR RCT) found experienced
  developers 19 per cent slower while believing they were faster.
  Structural decay is plausible and unproven; perceived speed is
  measurably unreliable.
- **Naming.** FRAG-CODING-13 found median 6.9 per cent agreement on
  names between developers, yet a chosen name is usually understood.
  That argues against enforcing naming uniformity in review and for
  reviewing only which concepts a name encodes.

## What should bind, default and be preferred

**Binding (a run fails without it).**

- Every change carries an executable oracle appropriate to its type,
  and the oracle exists before the implementation is accepted. FIX
  means a failing reproduction first (EV-0007, EV-0003).
- Behaviour is pinned before structure changes. Characterisation or
  approval tests before any refactor of code without a specification
  (FRAG-CODING-17).
- The error path is reviewed as first-class. FRAG-CODING-11 found 92
  per cent of catastrophic failures came from mishandling errors the
  software had already signalled, a third of them visible to plain
  inspection. Silent catch, bare except and swallowed errors are
  rejected.
- A machine security and policy gate runs diff-aware on every change
  before merge (FRAG-CODING-18, EV-0070).
- Failure modes callers may distinguish are declared, and the
  declaration is versioned with the interface (FRAG-CODING-12,
  FRAG-CODING-08).

**Default (applies unless the lock-book overrides with a reason).**

- Small changes, merged to trunk at least daily, no long-lived branches,
  no code freezes (FRAG-CODING-05).
- One reviewer, one iteration, approve on the health gradient rather
  than a perfection bar (FRAG-CODING-01, FRAG-CODING-02).
- Monorepo per venture until tooling cost forces otherwise
  (FRAG-CODING-09, FRAG-CODING-10).
- Refactor when a pending change demands it, not from a smell backlog
  (FRAG-CODING-14).

**Preference (record, do not gate).**

- Conventional Commits, and only where release automation consumes them
  (FRAG-CODING-07).
- Naming conventions beyond concept selection (FRAG-CODING-13).
- Duplication thresholds. Direction is worth instrumenting locally, the
  published magnitudes are not fact (FRAG-CODING-16).

## Refresh triggers

Re-run this domain on: an un-archive of or successor to
google/eng-practices; a peer-reviewed or empirical replacement for
FRAG-CODING-04; the next DORA report; an independent replication of the
GitClear structural metrics; a current-model replication of the CWE
scenario battery.
