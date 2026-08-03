---
summary: The four triggers that stop the pack and go to a human lawyer, what to hand over, and what to stop doing meanwhile
type: guide
tags: [security, pii]
kind: fact
scope: estate
sources: [FRAG-LEGAL-LICENSING-05, FRAG-LEGAL-LICENSING-13, FRAG-LEGAL-LICENSING-15, FRAG-LEGAL-LICENSING-16]
volatility: slow
review: 2028-03
review_by: 2028-03
---

# Reference: when to stop and instruct a lawyer

Level-three detail behind B7 in `packs/legal-licensing/PACK.md`. This
pack is routing. Everything below is the boundary where routing ends,
and crossing it with a confident answer is the most expensive mistake
available in this domain.

## The four triggers

**One. Copyleft code entering something we distribute or host in
modified form.** Detectable from the inventory and the deployment
shape. The reason it escalates rather than resolves: the licence text
does not say what counts as modification, nor where the program
boundary sits when the component runs behind an internal service
(FRAG-LEGAL-LICENSING-05). Those are the two questions people actually
have, and no source read answers either.

**Two. Any relicensing, licence change, or transfer of contributor
rights.** Changing an outbound licence, drafting a contributor
agreement, dual licensing, or accepting a contribution on unusual
terms. The reason: the decision binds everyone who came before and
cannot be undone by a later commit.

**Three. Personal data leaving the UK, or any regulator contact.** A
new sub-processor in another country, a transfer mechanism, a data
subject complaint that escalates, or any letter from the Commissioner.
The statute states what must be said in a notice and is silent on
whether a transfer safeguard is adequate for a specific arrangement
(FRAG-LEGAL-LICENSING-13).

**Four. Any letter alleging infringement.** Copyright, patent,
trademark or licence breach, from anyone, however informal the tone.
The reply is the thing being judged later.

## What to hand over

Escalation is only cheap if the facts are already assembled. The
handover is one page:

- What we do, in two sentences, and whether anything is distributed or
  reached over a network.
- The component or the data flow at issue, named exactly, with its
  identifier and version.
- The inventory entry and the decision record entry, if either exists.
- What we changed, if anything, and when.
- The specific question, phrased as a question rather than as a
  conclusion we would like confirmed.
- The date by which an answer changes what we do.

## What to stop doing meanwhile

- Do not merge the change that triggered it.
- Do not reason toward an answer in a commit message, an issue comment
  or a decision record. A written guess is discoverable and reads as a
  position.
- Do not reply to the letter or the regulator.
- Do not delete anything. Preservation is the default the moment a
  dispute is plausible.
- Do record the facts and the date. Facts are safe, conclusions are not.

## Two adjacent positions that are not escalations

**The EU market question.** Whether the venture places a product on
that market in the course of a commercial activity is a position to
record with reasoning, and to re-check before 2026-09-11 and before
2027-12-11 (FRAG-LEGAL-LICENSING-15). It escalates only when the
answer turns out to be yes and obligations attach.

**Authorship of agent-written code.** Unsettled, and staying unsettled
for now (FRAG-LEGAL-LICENSING-16). The response is to record
provenance, not to obtain an opinion. It escalates only if someone
asserts a claim over our output or we want to assert one over it.

## The failure this prevents

An agent that reasons its way from a licence text to a confident answer
about a modification boundary has produced something that looks like
advice, was never advice, and will be relied on anyway. The routing
rule exists because the detection is cheap and the error is not.
