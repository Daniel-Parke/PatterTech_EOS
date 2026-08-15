---
id: GD-DOCS-005
summary: Which documentation checks are allowed to fail a build, and which stay advisory
kind: wargame
type: wargame
tags: [ci, content, delivery, eos, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DOCS-001, DOC-DOCS-011]
applies_when: [publishes_docs]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0326, EV-0331, EV-0332, EV-0334, EV-0335]
review: 2028-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DOCS-005: Which documentation checks may block?

## Decision question and stakes

A documentation gate can run many checks. Making all of them blocking
produces a build that fails for reasons nobody cares about, and the
predictable end state is that the whole gate gets switched off. The
fork is where to draw the line, and it is a judgement rather than a
finding.

## Doctrines or coverage gap under pressure

- `DOC-DOCS-001` (default): Internal links and anchors resolve, checked in CI, and the check blocks.
- `DOC-DOCS-011` (default): External link checking is advisory, never blocking.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can the check fail for a reason unrelated to the change? Network,
  rate limits, a third-party outage.
- Is the finding objectively true or a matter of taste?
- Is the failure silent otherwise, meaning a reader is the only thing
  that would ever discover it?
- Who is on call for a red documentation build at three in the morning?

Applicability is `publishes_docs`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Everything blocks

Structure, links, prose, external URLs, the site build. Buys: nothing
rots. Costs: false failures from the network alone will bring the gate
into disrepute within a month, and taste findings block work that is
otherwise correct.

### B. Deterministic and offline checks block, everything else advises

Internal links and anchors, snippet execution, generated-file
regeneration, redirect verification, structural lint. Prose rules and
external links report without failing (EV-0331). Buys: a red build
always means something is actually wrong in the repository. Costs:
prose drift accumulates, and someone has to read the advisory output.

### C. B, with a promotion path

Same split, plus a rule that a prose finding can be promoted to
blocking once it has been observed against real changes and found not
to fire falsely (EV-0335). Buys: the gate tightens on evidence rather
than on ambition. Costs: someone has to run the promotion review.

### D. Advisory annotations only, nothing blocks

Every finding is surfaced in the change review as an annotation, and a
person decides. Buys: no false failures ever. Costs: findings get
scrolled past, which is the failure the annotation format was meant to
solve in the first place (EV-0332).

## Failure premises

### Premortem for A. Everything blocks

Assume `A. Everything blocks` was selected and the outcome failed. Test this option's stated failure mechanism first: false failures from the network alone will bring the gate into disrepute within a month, and taste findings block work that is otherwise correct.

### Premortem for B. Deterministic and offline checks block, everything else advises

Assume `B. Deterministic and offline checks block, everything else advises` was selected and the outcome failed. Test this option's stated failure mechanism first: prose drift accumulates, and someone has to read the advisory output.

### Premortem for C. B, with a promotion path

Assume `C. B, with a promotion path` was selected and the outcome failed. Test this option's stated failure mechanism first: someone has to run the promotion review.

### Premortem for D. Advisory annotations only, nothing blocks

Assume `D. Advisory annotations only, nothing blocks` was selected and the outcome failed. Test this option's stated failure mechanism first: findings get scrolled past, which is the failure the annotation format was meant to solve in the first place (EV-0332).

## Decision rule

- The check is deterministic, runs offline, and its failure means the
  repository is genuinely wrong: **blocking**. Links and anchors,
  snippet execution, regenerated files, redirects on rename.
- The check depends on the network: **advisory**, always (EV-0331).
- The check is about prose form: **advisory on arrival**, promotable
  under C once observed.
- The check is about whether content exists at all, such as a missing
  install section: **advisory, and escalate to a person**. Absence is
  the most damaging class practitioners report (EV-0326), and it is
  also the class a machine judges worst.

## Safe default

C. The split in B, plus a written promotion path so a house rule can
earn its way to blocking. New rules arrive advisory and stay there
until someone shows the false-fire rate is acceptable.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can the check fail for a reason unrelated to the change? Network, rate limits, a third-party outage.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. The split in B, plus a written promotion path so a house rule can earn its way to blocking. New rules arrive advisory and stay there until someone shows the false-fire rate is acceptable.

**Exit condition:** Stop or roll back the selected branch when false failures from the network alone will bring the gate into disrepute within a month, and taste findings block work that is otherwise correct, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can the check fail for a reason unrelated to the change? Network, rate limits, a third-party outage.

## Counter-evidence and transfer limits

### Preserved reasoning: The trap this guide exists to prevent

A repository installs a prose linter, makes it blocking on day one,
and now has a documentation gate that fails on heading case while the
quickstart is still wrong. That is the coverage-versus-style trade in
its most expensive form: the gate consumes the attention that would
have fixed the content, and it catches none of the failures that
actually reach a reader (EV-0326, EV-0335). Regex and word lists cannot
tell you a page is incorrect, incomplete or badly organised.

The mirror trap is the external link check. It is easy to add, it looks
like the same class of check as the internal one, and it fails on
somebody else's outage. Keep the two invocations separate so the
internal check can stay blocking when the external one is noisy.
### Preserved reasoning: What to copy from the largest worked example

One organisation runs structural lint, prose rules, internal link and
anchor validation across sibling repositories, diagram syntax, redirect
verification on rename, regenerated-reference verification and a
partial site build as blocking, and translated-content link checks as
explicitly non-blocking (EV-0332). The cheap and transferable parts are
link and anchor checking, redirect on rename, and regenerated-file
verification. The site build and the translation pipeline assume a
dedicated writing function and a CI budget a venture does not have.
The genuinely portable idea is surfacing findings as annotations inside
the change under review rather than only in a log, which is the
difference between a check people act on and one they scroll past. That
this organisation chose this split is not evidence that the split is
optimal, and the mechanical subset worth enforcing at all is small
(EV-0334).
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
