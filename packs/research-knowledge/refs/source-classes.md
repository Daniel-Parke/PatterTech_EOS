---
summary: What counts as a primary source for a software venture, the ladder for common source types, and where the borrowed hierarchy inverts
type: guide
tags: [data, content, product]
kind: fact
scope: estate
authority: default
review: 2029-10
sources: [EV-0534, EV-0545, EV-0547, EV-0171, EV-0259, EV-0260]
---

# Source classes for a venture

The three classes are defined by distance from the thing, not by
quality: a primary source is close to the event and usually written by
somebody involved; a secondary source sits at least one step removed and
adds thought; a tertiary source summarises the other two (EV-0545). B5
of `packs/research-knowledge/PACK.md` asks every source record to carry
its class. This file is the ladder for the source types a venture
actually meets.

## The ladder

| Source type | Class | Primary about what, exactly |
| --- | --- | --- |
| A specification or standard | primary | What conforming behaviour is defined to be. Never about whether anything implements it |
| Source code at a commit | primary | What this code does at this commit. Not about what the project intends |
| A licence file, a terms page | primary | What the terms say. Not about whether they are enforceable, which is `legal-licensing` |
| An API response, a real run, a reproduction | primary | The observed behaviour, on that date, in that configuration |
| Release notes, a changelog, a deprecation notice | primary | What the maintainer says changed and when |
| Maintainer documentation | primary about intent, secondary about behaviour | What the maintainer means it to do. Documentation and implementation part company routinely |
| A vendor blog or launch post | primary about intent, secondary about behaviour, and an interested party throughout | What the vendor wants understood |
| A published study | primary about its own result | The finding it measured, under its own population and design |
| A conference talk, a practitioner post, a book | secondary | Somebody's reading of a primary source |
| An answer site, a summary page, a model's answer | tertiary | A summary of secondary readings, at unknown distance from anything |
| A search result snippet | not a source | It was written by a ranking system. Follow it to the thing |

## The inversion, which is the point of this file

The borrowed policy is cautious about primary sources: use them for
straightforward descriptive statements, and get a secondary source
before interpreting them (EV-0545). That policy was written for an
encyclopedia that forbids original research outright, which is the
opposite of a venture that has to reach and act on its own conclusions.

For a venture the ordering partly inverts. The specification and the
source are the most reliable things available, and the secondary reading
is usually where the error entered. Importing the caution unexamined
pushes a venture towards blog posts about specifications and away from
specifications, which is the failure this pack is against.

What survives the inversion, and what B5 actually asks for, is the
second half of the rule. A conclusion drawn from reading a primary
source is a finding of the venture's, recorded as the venture's, at
whatever certainty it has earned. It is not attributed to the source. A
specification that is silent on a case has not endorsed the reading
somebody drew from its silence.

## Reading the class off a source, in practice

Three questions, in order.

1. **Who wrote it, and what were they in a position to know?** A
   maintainer knows their intent. Nobody, including the maintainer,
   knows the behaviour without running it.
2. **What is it primary about?** Almost nothing is primary about
   everything. The table above splits several rows for that reason, and
   the split is where most misclassification happens.
3. **Is the author an interested party in the claim?** Vendor material
   about the vendor's own product always is. That does not make it
   unusable; it is still the primary statement of intent. It makes it
   evidence about the vendor rather than about the world, and a claim
   about behaviour needs an independent route as well.

A source stating which of its own pages should be trusted, or which
sources a reader should prefer, is the sharpest case of question three
(EV-0547). It is primary evidence about what the source wants believed,
and no evidence at all about which pages are correct. GD-RESEARCH-004
argues what to do about it.

## Where the class changes underneath you

A primary source is primary at a version. Three signals move it.

A version number carries meaning only once a public interface has been
declared, and a major-zero version is an explicit statement that
anything may change at any time (EV-0171). A record citing a major-zero
project without pinning a commit has cited nothing durable.

A retirement notice tells you a primary source is becoming a historical
one on a stated date, and the good publishers give both the deprecation
date and the date the thing stops answering (EV-0260). Both dates belong
in the record.

The hardest case is the source that keeps its identity and changes its
behaviour. A model endpoint behind a stable name moved substantially in
months, and not uniformly in the direction of improvement (EV-0259). For
that class, an observation is primary about one date and about no other
date, and the record has to say so or the claim silently becomes false.

## What the hierarchy does not settle

The Oxford levels are published with the caveat that hierarchies have
been used inflexibly, that levels move up and down for quality,
imprecision and indirectness, and that no ranking scheme works unless
judgement is applied to its output (EV-0534). The class is an input to
weighing a claim and never the answer. A careful secondary reading of a
specification beats a careless run of the code, and the class field will
tell you the opposite. That is what the grade on the claim is for.
