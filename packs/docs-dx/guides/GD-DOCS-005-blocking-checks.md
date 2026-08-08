---
summary: Which documentation checks are allowed to fail a build, and which stay advisory
type: guide
tags: [content, delivery, ci, tooling]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0326, EV-0331, EV-0332, EV-0334, EV-0335]
review: 2028-04
---

# GD-DOCS-005: Which documentation checks may block?

## The question

A documentation gate can run many checks. Making all of them blocking
produces a build that fails for reasons nobody cares about, and the
predictable end state is that the whole gate gets switched off. The
fork is where to draw the line, and it is a judgement rather than a
finding.

## It depends on

- Can the check fail for a reason unrelated to the change? Network,
  rate limits, a third-party outage.
- Is the finding objectively true or a matter of taste?
- Is the failure silent otherwise, meaning a reader is the only thing
  that would ever discover it?
- Who is on call for a red documentation build at three in the morning?

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

## Default

C. The split in B, plus a written promotion path so a house rule can
earn its way to blocking. New rules arrive advisory and stay there
until someone shows the false-fire rate is acceptable.

## The trap this guide exists to prevent

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

## What to copy from the largest worked example

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

## Worked rulings

- **PatterTech EOS docs-dx pack (2026-08, argued)**: C. Deterministic
  offline checks block, prose and external advise, promotion allowed on
  observed evidence. Argued from EV-0331 for the network split and
  EV-0326 for the coverage-first ordering.
- **PatterTech EOS itself (2026-08, inherited)**: the repository checker
  already splits errors from warnings and blocks only on errors, with
  voice findings as warnings. Inherited from the checker's severity
  model.
