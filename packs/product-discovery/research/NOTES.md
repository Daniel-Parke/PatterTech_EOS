---
summary: Research synthesis for the product-discovery pack, four schools of discovery, what the evidence actually supports, and what should bind
type: example
tags: [eos, testing]
---

# Product discovery pack research notes

Cutoff 2026-08-03. Eighteen new sources in `sources.fragment.json`,
plus existing ledger records cited by EV id. The domain question is
not what good discovery looks like in a funded product org. It is:
when building a thing costs an afternoon of agent time, what is
discovery still for, and which of the inherited frameworks survive
that cost collapse.

The headline for the whole pack: this domain has far worse evidence
than the engineering packs. Most of what circulates as product
discovery method is consultancy practice published as blog posts,
never independently evaluated, and often built on statistics whose
provenance nobody checked. Two of the eighteen sources are controlled
work that directly contradicts widely taught rules. That gap is the
most important thing here and it should shape how much the pack is
allowed to bind.

## Four schools, and when each fits

**1. Phase-gated discovery.** A named, time-boxed phase before any
building, with defined exit artefacts. FRAG-01 is the strongest
written version: four to eight weeks, no building during it, exit only
with a problem statement that is not a disguised solution, named
constraints, a map of what already exists, and a stated measure of
success. Its best idea is that stopping at the end of discovery counts
as a successful discovery, which makes the kill option part of the
definition rather than an embarrassment. FRAG-09 gives the same shape
a vocabulary, diverge then converge, twice, with the separation of the
two modes in time being the only rule in it that does real work.
Fits: irreversible commitments, anything with a regulatory or data
boundary, anything where the wrong problem statement costs months.
Anti-pattern: running a four-week discovery on a change an agent could
build and instrument in a day. The phase length was calibrated for
teams whose build step was the expensive part.

**2. Continuous discovery.** No phase, a standing cadence. FRAG-13 is
the reference version: one outcome at the root, opportunities admitted
only when grounded in a story from an actual interview, effort
deliberately excluded when comparing opportunities so cheapness cannot
pose as value, and at least three candidate solutions carried per
opportunity so the first idea is never compared against nothing.
FRAG-14 gives the complementary completion test, four risks with
separate owners: value, usability, feasibility, viability. Discovery
is finished when all four are retired, not when a document exists.
Fits: a live product with reachable users and a running metric.
Anti-pattern: a solo operator holding all four risks will test the two
they find interesting and assume the other two away. In practice
viability is the one that goes untested.

**3. Outcome and job elicitation.** Get underneath the feature request
to something that survives a change of technology. FRAG-16 is the
purest form and its genuine contribution is the unit of analysis, a
desired outcome written as a measurable statement about a step in the
user's job. A feature request expires when the technology moves and an
outcome statement does not. Fits: anywhere you expect the
implementation to churn, which under agentic development is
everywhere. Anti-pattern: the scoring half. Adding an importance
rating to the difference between importance and satisfaction has no
stated justification, needs 180 to 600 survey respondents nobody early
has, and every published claim about its effectiveness comes from the
firm that sells it. Take the elicitation, leave the arithmetic.

**4. Build and measure.** Skip the investigation, ship the smallest
real thing, read the instrument. FRAG-03 is the empirical backbone:
across a large corpus of randomised online experiments, roughly a
third of ideas moved the target metric positively, a third were flat,
and a third were negative, with the search property doing worse still.
Expert judgement inside the team does not predict which third an idea
lands in. Fits: reversible changes on a surface with enough traffic to
power a test. Anti-pattern: FRAG-04, the same lead author, catalogues
how naive experimentation manufactures confident wrong answers. An
experiment counts as evidence only if the stopping rule, the metric
and the segmentation were fixed before the data arrived. A test at low
traffic is theatre with statistics attached, and EV-0059 is the
existing ledger record for writing decision rules down before the
readout.

## The disagreements that are load-bearing

**How many people do you need to talk to.** FRAG-06 is the source of
the five-user convention: given a fixed budget, three rounds of five
beat one round of fifteen, because each round changes the design and
so changes the problem set. FRAG-05 tested that empirically with sixty
participants and resampled. Random sets of five found anywhere from 99
per cent down to 55 per cent of the known problems. Ten raised the
floor to about 80, twenty to about 95. These are not really in
conflict about the data, they optimise different things: FRAG-06
optimises expected problems found per pound across iterations, FRAG-05
measures the variance that the expected value hides. The resolution
that binds is to reason about the worst case, because you only ever
draw one sample and cannot tell which one you drew. Also note that
FRAG-06 is twenty-six years old, never revised, and is routinely cited
to justify five customer interviews, which is a completely different
activity from the usability defect-finding it models. FRAG-02 adds the
sharper point: the recruitment frame, not the participant count, is
what makes a discovery wrong.

**Does spec-driven development work.** EV-0074 and EV-0075 present
spec-driven development as an established improvement, with the
specification becoming the artefact that generates the code. FRAG-12
is a Stage 1 registered report on exactly that question, protocol peer
reviewed and accepted at SANER 2026, with no results collected at the
cutoff. So at 2026-08-03 the controlled evidence for the central
claim does not exist. The spec-kit repository is itself explicit that
it is experimental. FRAG-07 is the one part of the specification
tradition with real pedigree: the EARS clause order, developed on
airworthiness regulations for jet engine control, where a requirement
that cannot be written in the template usually turns out to be a wish,
a design decision, or two requirements stuck together. The forcing
function is real and it is about form only. It cannot tell you whether
the requirement should exist.

**Can a model do the research.** FRAG-10 found that the best of four
conditions was human collaborative discussion followed by LLM
synthesis of the transcript, beating both unaided collaboration and
direct model generation, scored against ISO/IEC/IEEE 29148 criteria.
FRAG-11 benchmarked LLM-simulated survey respondents against the
General Social Survey and World Values Survey and found no model beat
even the strongest non-LLM baseline at the individual level, models
over-determined demographics, and on segment targeting they inflated
between-segment gaps two to fourfold and would have pointed a team at
the wrong segment in half the US cases. Read together these are one
finding, not two: give the model the structuring job on real human
input, never the origination job on invented input. The 29148 caveat
matters as well, since conformance to a documentation standard
rewards well-formed prose and cannot detect a well-written requirement
for the wrong thing.

**How much gets built that nobody uses.** The famous number, 64 per
cent of features rarely or never used, traces via FRAG-17 to a 2002
keynote reporting on four internal applications, repeated for two
decades by people who never checked. FRAG-18 reaches a similar
magnitude from instrumented telemetry, but it is vendor research with
a commercial interest in the answer, no published methodology for what
counts as a feature or as used, a sample confined to firms that bought
product analytics, and seven years stale. The direction is well
supported and the magnitude is not. Cite it with the vendor label
attached every time.

## What should bind, default, and stay preference

**Binding.** Every discovery artefact states the decision it is meant
to unblock and the observation that would change that decision, in
the goals-signals-metrics order of FRAG-08. A proposal with no named
signal is untestable. Every number used to justify work carries its
own provenance record, which is the procedural lesson of FRAG-17 and
the reason this repo has an evidence ledger at all. Any claim about a
user population that came from a model rather than a person is
labelled as such, per FRAG-11. Any experiment declares its stopping
rule, metric and segmentation before data arrives, per FRAG-04. Kill
is a legitimate discovery outcome and must be an explicitly available
verdict, per FRAG-01.

**Default.** Retire all four of the FRAG-14 risks explicitly, with
viability written down rather than assumed, since that is the one a
solo operator skips. Elicit outcomes rather than features, per
FRAG-16. Write acceptance criteria in EARS clause order once the
problem is settled, per FRAG-07. Carry more than one candidate
solution before committing, per FRAG-13. Separate diverging from
converging in time and say which you are in, per FRAG-09.

**Preference.** The specific numbers. Four to eight weeks, five users,
three candidate solutions, three to four interviews per revision, RICE
confidence tiers of 100, 80 and 50. None of these has evidence behind
the exact value. FRAG-15 is honest that RICE is not a rule, and its
one genuinely useful element is the explicit confidence multiplier
that forces a team to write down how much of the score is guesswork.
The rest multiplies three subjective estimates into a precise-looking
number with invisible error bars, and FRAG-03 shows the impact term it
leans on hardest is close to uninformative at the idea level.

## Open questions, honestly

The pack should not pretend to answer these.

- Nobody has measured whether the one-third success base rate of
  FRAG-03 holds for agent-generated ideas. It may be better because
  volume is cheap, or worse because the model regresses to the common
  case. There is no data either way at the cutoff.
- The whole discovery literature was written when building was the
  expensive step. No source located reprices discovery against a build
  cost near zero. EV-0010 is the closest signal that intuitions about
  agentic speed are unreliable, and EV-0153 is the nearest structural
  analogue, build the simple thing first and let the evidence force
  the split.
- Nothing found says at what traffic level experimentation stops being
  theatre and starts being evidence, in a way that a venture with
  hundreds rather than millions of users could apply.
- Whether specification-first improves anything is genuinely open, see
  FRAG-12. The pack should teach the EARS discipline on its own
  merits and not borrow authority from the spec-driven claim.
