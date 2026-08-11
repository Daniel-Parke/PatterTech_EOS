---
summary: How the swarm pack was assembled, what the corpus disagrees about, and the questions it could not close
kind: record
scope: eos-internal
type: guide
tags: [eos, arch]
review: on-change-of:packs/agentic-swarm
---

# Research notes: agentic swarm

## Where the material came from

Six commissioned research reports, run on 2026-08-10 for ADR-0006
decision 4, covering graph orchestration, decomposition and scaling,
verification without test-first ordering, context and budgets, review
and quality, and frontier risks. Together they carried 232 sources with
licences, findings, applicability limits and counter-evidence, plus
candidate rules already graded binding, default or preference.

`packs/agentic-swarm/research/sources.fragment.json` carries 52 of
those 232, chosen on one rule: a source is in the fragment file if the
pack, its guides, its references or its checks make a claim that rests
on it. The other 180 are context, corroboration or leads the reports
themselves marked unverified, and they stay in the reports. That
matches house practice, where existing packs carry twelve to
twenty-seven ledger rows each.

## How the rules were graded

ADR-0008 sets the test: a rule stays binding only if it prevents a
concrete failure that is serious or hard to reverse, and its basis is
law, standard or empirical evidence, or it is a protected-set safety
floor. Ten of the candidate rules cleared it. Several that the research
proposed as binding did not, and were demoted with the reason visible
in the pack:

- **Partition the failure surface** became D4. The failure is real and
  the mechanism is clear, but the evidence is one vendor case study,
  and the cost of getting it wrong is a wasted run rather than a bad
  merge.
- **Three to five lanes** stayed a default and is labelled in the pack
  as a converging heuristic rather than a measured optimum, because no
  published study varies lane count on real repositories and measures
  pass-at-merge.
- **Observability rules** did not become pack law at all. Tracing is
  already binding in `packs/agentic-development/PACK.md` B6, and the
  span vocabulary this domain would add sits in a convention whose
  documents are all marked Development status, so fixing names here
  would date the pack. What survives is the observation that no
  standard attribute exists for the delegation chain, recorded in the
  risk register rather than as a rule.
- **Cache and pacing economics** were left out of the body entirely.
  They are real and they are cost rules, not correctness rules, and
  every number in them is a vendor number that moves. They belong in a
  venture profile.

## What the corpus disagrees about

**Whether agent-written changes destabilise trunk.** One merge-queue
dataset of 153,000 merges found AI-assisted changes broke main at 1.9
per cent against 4.4 per cent for unassisted, holding within the same
repositories. Vendor telemetry over 22,000 developers found bugs per
change up 54 per cent under high adoption. Both cannot be
straightforwardly true of the same population. The likely reconciliation
is that one measures merge-queue-protected repositories and the other
measures adoption broadly, but neither source establishes that, so the
pack records the disagreement rather than picking a side.

**Whether wide fan-out works.** One optimistic scaling law finds
collaborative emergence at about sixteen agents and saturation near a
hundred. One budget-controlled study finds per-agent reasoning
prohibitively thin beyond three or four. The reconciliation the pack
uses is that the optimistic result was measured on short-horizon
generation with no repository merge gate, which is exactly the
constraint that makes lane count expensive here.

**Whether review can move to the end.** The position that coding agents
supersede human inspection is argued in the literature, and its own
authors list unresolved objections including prompt injection against
reviewing agents with no fully solved defences. Against it, the
strongest counter in the corpus is a controlled factorial result
showing that restoring the specification recovered the whole
single-agent ceiling while conflict reports added nothing. The pack's
answer is to spend on the specification first and keep independence of
the checker, and to make no claim about when review happens.

## Questions the research could not close

1. **No public benchmark measures a ten to fifty node dependency-graph
   build with a single integrator.** The architecture this pack
   describes is evidenced by one partitioning study, one vendor case
   study and product documentation. The EOS's own runs will be the best
   evidence it has, which is why journalling and stating n are pack
   rules rather than aspirations.
2. **No measured catch rate for clean-context reviewer agents on
   realistic multi-file changes.** The nearest study is 116 single-file
   competitive-programming tasks. This is the largest evidential hole
   and it sits directly under D8. The mechanism evidence for reviewer
   independence is solid; the catch rate is not claimed.
3. **No study measures defect escape for a full swarm-plus-integrator
   pipeline against a controlled baseline.**
4. **No published defence against social engineering of review agents.**
   The attack is measured across about 1,062 adversarial changes with
   no mitigations tested, so B4 is inference from the attack surface.
5. **Conflict rates as a function of lane count.** The measured rates
   are per-pair, textual only, and the authors call them a conservative
   lower bound. Any quadratic growth argument from them is arithmetic
   under an independence assumption that is probably optimistic.
6. **Four source PDFs did not extract cleanly** in the underlying
   research, including one on merge conflicts between parallel coding
   agents. If a merge-conflict rate ever becomes load-bearing for a
   binding rule here, that source is the one to read properly first.

## Provenance and reuse

Every fragment record carries its own licence as a recorded fact rather
than a class assumption. Several sources are restrictively licensed:
one taxonomy is CC BY-NC-ND, which permits citation but not adapting
its text; one practitioner post is CC BY-NC-SA; several vendor pages
state no reuse licence at all. Nothing in this pack reproduces text
from any of them. Where a number appears, it is a fact cited to its
source, not carried expression.

## Citation state, and what the import did

At authoring time the pack body cited `FRAG-` ids, because the evidence
ids did not exist yet. They are assigned by
`tools/import_fragments.py`, which runs once every lane has landed its
fragment file. That import has since run, the body now cites the
assigned `EV-` ids, and the only FRAG ids left in the pack are in this
directory, which check S014 exempts as the pre-import record. On the
committed partition the ledger and the import belonged to the registry
lane, T-0025, rather than to the integrator; the exemplar records that
and what it cost.

Six of the 52 records matched a URL already in `registry/evidence.json`,
so the import merged them rather than assigning new ids, and the pack
cites the existing rows instead: EV-0013, EV-0053, EV-0108, EV-0109,
EV-0112 and EV-0244. The other 46 arrived as EV-0450 to EV-0495.

A merge keeps the older row's finding text, and for five of the six that
text is thinner than the fragment record it absorbed. Each is cited in
the pack for something its ledger row does not say:

- **EV-0013**, in the risk register, for the span convention defining no
  delegation-chain attribute. The row carries the conventions and their
  development status, not the gap.
- **EV-0053**, in D4 and D5, for coordination through claim files in git
  and for sixteen agents hitting identical bugs on one monolithic build.
  The row carries the sixteen-lane run and the verifier constraint.
- **EV-0108**, in B2, B9 and the risk register, for the lead's history
  not carrying over, for two teammates on one file overwriting each
  other, and for the permission-skipping flag. The row carries the
  shipped coordination primitives and the three-to-five guidance.
- **EV-0112**, in B6, for the fifteen times token multiple, which the
  row does carry, and until this correction for token usage explaining
  about 80 per cent of performance variance, which it does not. That
  second claim has been taken out of B6.
- **EV-0244**, in the risk register, for one model family dropping 30 to
  45 per cent as irrelevant context grew from about 300 to about 113,000
  tokens. The row carries the shape of the effect without the figures.

EV-0109 is the exception: its row carries what B3 cites it for. Every
fact above sits in `sources.fragment.json` beside these notes, under
FRAG-AGENTIC-SWARM-50, -13, -14, -12 and -25. The repair is to enrich
those five ledger rows so they carry the older statement and the newer
one, which is a change to `registry/evidence.json` and belongs to
whoever holds that file.
