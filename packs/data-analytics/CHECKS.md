---
summary: What a reviewer or a checker can verify about analytics, modelling and experiment work, split into executable today and judgement
type: guide
tags: [data, testing, delivery]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0056, EV-0057, EV-0059, EV-0139, EV-0225, EV-0313]
review: 2027-08
---

# Data and analytics pack checks

The evaluation criteria for work under `packs/data-analytics/PACK.md`.
Each row names what is verified, how, and whether a machine can do it
today. A check that needs a person is still a check; it is just a
person's job.

## Executable today

These run in CI, or against the delivered tree, with no human input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | A contract or expectation file exists for every published model | File presence per model in the marts layer, and the file parses | D9 |
| C-02 | The contract carries all five elements | Key presence for schema, quality rules, freshness, owner and support path | D9 |
| C-03 | The gate blocks rather than reports | The pipeline command exits non-zero when a quality rule is violated, and the publish step is downstream of the check | D10 |
| C-04 | The gate was actually run | The check step appears in the build's dependency graph, not only in the repository | D10 |
| C-05 | No identifying column in the analytics layer | Column-name scan of published models against a pattern for email, name, phone and postcode, plus a value scan for address-shaped strings | B3 |
| C-06 | Every identifying column that survives has a recorded basis | Every match from C-05 resolves to a lawful-basis record naming that column | B3 |
| C-07 | Event names follow the taxonomy | Every name in the tracking plan matches object then past-tense action, contains no digit and contains no identifier | D1 |
| C-08 | Event names are unique and mapped | No duplicate names, and every raw source event maps to exactly one plan entry | D1, D9 |
| C-09 | The fact grain is declared in words | A grain statement exists per fact model and names one row per something | D11 |
| C-10 | The grain is enforced | A uniqueness rule on the declared grain columns exists and passes | D11 |
| C-11 | Layer discipline | No marts model selects directly from a source, and no staging model contains a join | D2 |
| C-12 | Pre-declaration exists before traffic | A file naming the randomisation unit, the primary metric and the stopping rule is committed before the first assignment timestamp in the data | B4 |
| C-13 | Sample ratio mismatch is computed | The analysis output contains observed counts, expected counts and a computed p-value for the assignment ratio | B5 |
| C-14 | A failed ratio check voids the result | When C-13 reports a failure, no decision verb appears unaffirmed in the written answer | B5 |
| C-15 | Contract scope | No private staging or intermediate model carries a contract | D6 |
| C-16 | Retention has a job | Every table with a stated retention period has a scheduled deletion step | B3 |
| C-17 | Compatibility mode is declared | Any event stream a consumer replays from its start declares a transitive compatibility mode (EV-0139) | D1 |

C-14 needs a concrete form to be executable. The one this pack uses:
search the written answer for a decision verb such as ship, roll out,
launch or winner, and require that every occurrence sits inside a
negated clause in the same sentence. Zero unaffirmed occurrences passes.

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The grain statement is the grain the model actually has | Reviewer, because a uniqueness rule can pass on the wrong columns | D11 |
| J-02 | The quality rules cover the failures this table can actually have | Reviewer, because a suite checks what you declared, not what you forgot (EV-0056) | D9, D10 |
| J-03 | A suggested constraint does not encode a current bug as the norm | Reviewer, on every derived rule before it is accepted | D10 |
| J-04 | Semantic drift has not happened under a passing contract | Reviewer, on any unexplained metric step change | D10 |
| J-05 | The identifier rung chosen is the lowest that answers the question | Reviewer, against the ladder in `packs/data-analytics/refs/PRIVACY_IN_ANALYTICS.md` | B3, D8 |
| J-06 | The minimum effect worth detecting is the one that would change a decision | Reviewer, before the sample size is computed | B4 |
| J-07 | The experiment was reachable at all | Reviewer, comparing required sample size to assignable traffic and to the window in which the answer matters | D4 |
| J-08 | The stopping rule was followed, not chosen afterwards | Reviewer, against the pre-declaration from C-12 | B4 |
| J-09 | Causal language is used only where assignment was randomised | Reviewer, on every written claim from analytics | Outcomes |
| J-10 | A large effect was checked for instrumentation error before being believed | Reviewer (EV-0313) | B5 |
| J-11 | Two models do not compute the same business number by different routes | Reviewer, across the marts layer | D2 |
| J-12 | The storage choice matches the measured working set | Reviewer, at the review trigger rather than continuously | D5 |
| J-13 | The tracking plan has an owner who is still there | Reviewer, at each review date | D9 |

## Which checks map to the pack drill

The acceptance drill for this pack, `DRILL-DATA-001`, is satisfied by
C-01 and C-02 (drill criteria 1 and 2), C-03 and C-04 (criterion 3),
C-05 (criterion 4), C-07 (criterion 5), C-09 (criterion 6), C-13
(criterion 7), C-14 (criterion 8) and J-08 with C-12 (criterion 9).
Criterion 10 is the repository checker and is not this pack's rule.

## How to read a failing check

C-03 failing while C-01 and C-02 pass is the highest-signal failure in
this pack: a contract exists and never runs. Log it separately, because
it looks like compliance in a file listing.

C-13 passing while C-14 fails is the failure this pack exists to stop.
The check was computed, the failure was seen, and the decision was taken
anyway. Treat it as a stop rather than a finding.

C-05 failing means source columns were copied forward without anyone
asking what the analytics layer is allowed to hold. It is cheap to fix
at staging and expensive to fix after six months of history.

## What this pack deliberately does not check

- Query performance or cost. Real concerns, owned by nobody here.
- Dashboard layout and visual design, which sit in
  `packs/ui-ux/PACK.md`.
- Migration mechanics for a schema change, which sit in
  `packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md`.
- Which contract format, quality tool or dashboard method was used. All
  preferences.
- Absolute model count or layer count. Only the discipline within them.

## Wiring note

C-05, C-07, C-12 and C-13 are the four checks a venture has to configure
before this pack has teeth, because each needs a pattern list, a plan
file location or a statistical helper pinned in the venture's own gate
configuration. C-01 through C-04 come free with any transformation tool
that supports contracts. Nothing here runs until those four are written
down.
