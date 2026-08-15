---
summary: In the repository under the code gate, an open wiki with a policy, a curated store with one editor, or no separate base at all?
type: guide
tags: [data, content, delivery]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2029-05
sources: [EV-0539, EV-0540, EV-0546, EV-0547, EV-0548, EV-0055, EV-0097, EV-0331]
---

# GD-RESEARCH-002: where does the knowledge base live, and who may write to it?

## The question

A venture that researches produces findings, and findings have to land
somewhere other people will find them. Where they land decides two
things that look separate and are not: how much friction a writer meets,
and how much trust a reader may place in what they read. Every mechanism
that raises one lowers the other, and a venture that does not choose
gets the worst pairing by default, which is a store anyone may write to
and nobody may rely on.

The fork is not the tool. It is who carries the burden of sourcing, and
what happens to a claim that does not carry one.

## It depends on

- How many people write, and are they the same people who read?
- Is the base read by anyone outside the venture, now or later?
- Does the venture already have a review gate that findings could ride
  through, or would this be a second gate?
- What happens to a claim when it is challenged: is there history to
  restore from, or is deletion final?
- Does the base need to be readable by machines, or only by people?

## Options

### A. In the venture's repository, under the same gate as the code
Findings are files, changes are pull requests, and the merge gate that
already exists reviews them. Buys history for free, so a claim removed
can be restored, which is what makes the burden rule survivable
(EV-0546). Buys the mechanical checks with no extra machinery: schema
validation on the source records, a link check on a schedule (EV-0331),
and citation metadata that travels with the artefact (EV-0540). Costs
friction for anyone who does not work in the repository, which in most
ventures is everyone who is not an engineer, and that friction is
exactly where findings stop being written down.

### B. An open wiki with a written policy
Anyone may write, the burden of citation sits on whoever adds or
restores a claim, uncited material may be challenged and removed, and a
dispute process exists. Buys the lowest possible friction on the write
path and a governance model with decades of adversarial use behind it.
Costs the assumption that removal is cheap: the policy works because the
history holds the text, so a wiki without real history turns the removal
rule into evidence destruction. Costs the assumption of volume too, and
a policy written for a project with thousands of editors is heavier than
three people need.

### C. A curated store with a named editor
One person, or a small named set, may write. Everyone else proposes.
Buys consistency and a single throat to ask, and it is the only option
where the classification of sources stays coherent without a checker.
Costs a bus factor and a bottleneck, and the editor becomes the slowest
part of every research question. Costs contributions too: a proposal
queue that runs a week long stops receiving proposals.

### D. No separate base; findings live only in decision records
Every finding is written into the decision it supported, sized to that
decision (EV-0097), and there is nothing else to maintain. Buys the
lowest maintenance cost available and guarantees no finding rots unread,
because there is nothing to read. Costs re-use entirely: the same
question gets researched again next quarter because nobody can find last
quarter's answer, and there is no place at all for a finding that did
not settle a decision, which includes every piece of counter-evidence.

## Decision rule

- The venture is a repository and the writers are the engineers: A.
- Non-engineers write findings regularly, and the venture has real
  history and restore in whatever tool they use: B, with the burden rule
  written down and removal replaced by marking.
- The findings will be read by somebody outside the venture, or the
  classification of sources is load-bearing for a claim the venture
  makes publicly: C on top of A. The gate is the editor, the store is
  still the repository.
- One person, one quarter, no expectation of re-use: D, and say out loud
  that it is a choice to lose the findings.
- Any of the four: reading is open. A knowledge base that is hard to
  read has already failed, whatever its write path looks like.

## Default

A, with B's burden rule. The findings live in the venture's repository
under the gate the code already goes through, and the person adding or
restoring a claim owes the citation. A claim that needs one and lacks it
gets marked unsourced and stays visible, rather than being deleted,
because in most venture bases deletion loses the only copy.

The record is the durable artefact and outlives the source, which is
what A buys and what makes the base still worth reading after the pages
it cites have gone (EV-0539).

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: A throughout. The evidence
  ledger, the lessons ledger and every pack's research directory are
  files in the repository under the merge gate, and the integrator is
  the only writer to the shared registries, which is C layered on A for
  the registries alone. The reason for the layer is deduplication of
  source ids across parallel lanes, not editorial control.
- **PatterTech EOS (2026-08, argued)**: D rejected. The estate's
  decisions live in ADRs and its findings live in a ledger, deliberately
  apart, because the counter-evidence that settles nothing today is the
  material that settles something in a year.
- The GitLab handbook is the strongest published instance of A taken to
  its limit, where the handbook is the working artefact and gaps are
  fixed at the point of discovery (EV-0055). It evidences that the
  pattern scales; it does not evidence that a small venture should copy
  the whole of it.
- No venture ruling yet.

## Counter-evidence

The burden rule is imported from a project whose enforcement half is
heavier than a venture needs, and whose removal rule depends on an
assumption most ventures do not satisfy (EV-0546). Taking the rule and
dropping the removal is this estate's adaptation, not a finding, and
nothing measures whether marking works as well as removing.

A knowledge base that publishes its own navigation to machine readers is
making a claim about which of its pages are authoritative (EV-0547), and
a venture that publishes one is doing to somebody else what
GD-RESEARCH-004 says not to accept. The one practitioner review
available records that no major provider documents reading such a file
at inference time and that its presence had no measurable effect on
citation (EV-0548). Publish one if it helps a human reader navigate. Do
not count on it being read, and do not put instructions in it.

Nothing here is evidenced against the outcome that matters. No source
measures whether a venture that keeps a knowledge base decides better
than one that does not, and the estate's own practice is one instance
with no comparison.
