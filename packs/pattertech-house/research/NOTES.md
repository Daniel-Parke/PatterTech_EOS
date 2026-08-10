---
summary: Three competing visual-language philosophies, what the evidence supports, and where the PatterTech house style is taste rather than fact
type: example
tags: [eos, testing]
---

# PatterTech house style: research notes

The domain is taste, carried forward from `archive/v1-final:doctrine/web-design`.
Taste cannot be proved, but the mechanisms underneath it can be. These notes
separate the parts of the house language that rest on measured behaviour, the
parts that rest on a defensible default, and the parts that are simply ours.

## The three philosophies in play

### 1. Systematic design-system orthodoxy

Tokens in layers, primitives that components consume, accessibility as the
first gate, a component per job, evidence of use before a pattern is admitted.
This is GOV.UK (EV-0062, EV-0063), USWDS (EV-0064), Carbon (EV-0227), Polaris
(EV-0238), Radix and shadcn as the unstyled substrate (EV-0066, EV-0067), and
the Design Tokens format and Style Dictionary as the plumbing (EV-0030,
EV-0065). Behaviour patterns come from the ARIA Authoring Practices (EV-0028,
EV-0029), the floor from WCAG 2.2 (EV-0027) and axe-core (EV-0236).

Fits when many hands touch the surface, when the surface is transactional, or
when the cost of a wrong interaction is high. Trades away distinctiveness on
purpose: the WebAIM Million (EV-0235) is the standing reminder that most sites
fail the floor, so a system that guarantees the floor is already doing more
than most. Anti-pattern: treating the system as the design, so every page is a
well-tokenised page nobody remembers.

### 2. Editorial-instrument taste (the house style)

Content picks its container: ledger for parallel facts, plaque for numbers,
panel only for genuinely self-contained things, prose for reading matter. A
mono annotation voice carries indices, kickers, captions and meta. Sections
open flush left with numbered furniture. Light is graded into field, conduit,
bloom and radiance with alpha budgets. The nearest public relative is the
Guardian's Source (EV-0239); NN/g's account of flat design (EV-0234) is the
warning about what happens when restraint removes affordance too.

Fits long-form argument, technical marketing and anything meant to read as a
document under instrumentation. Trades away speed of authoring: every section
requires a judgement the card grid would have made for you. Anti-pattern:
executing restraint as absence, which the archive records as the v4 failure,
elegant and invisible.

### 3. Expressive and embellished

Motion and ornament as the point, not the residue. Expressive Material Design
(EV-0232) is the current platform-scale statement of it, and the empirical
support is Bateman et al. (FRAG-PATTERTECH-HOUSE-03): embellished charts cost
nothing in interpretation accuracy and gain in long-term recall.

Fits when the job is to be remembered rather than to be read precisely, and
when the surface is short. Trades away density and accessibility headroom.
Anti-pattern: the generic tell, where expressiveness converges on the same
gradient-and-glow vocabulary everyone else generates.

## The disagreements that actually bite

**Restraint versus memorability.** Doctrine 1 says quiet beats loud. Bateman
says decorated charts are remembered better at no accuracy cost. Both can hold
if the jobs are split: figures that must be read precisely stay austere, and
one figure per piece is allowed to be the memorable one. What the house should
not do is claim restraint improves comprehension, because that is not what the
evidence says.

**Dark register versus legibility.** The house ground is a dark void. The
polarity literature (FRAG-PATTERTECH-HOUSE-05) and NN/g's synthesis
(FRAG-PATTERTECH-HOUSE-06) both report a positive-polarity advantage for
readers with normal vision, concentrated in small type. The house leans hard on
small type: mono kickers at roughly 0.7rem with 0.2em tracking are precisely
the condition where the penalty is largest. This is the sharpest contradiction
in the pack. It does not kill the dark register, but it means the annotation
voice must be bought back with size, weight and measured contrast, and a light
register must be a supported variant rather than a promise.

**Contrast maths.** The archive records text tiers as WCAG 2 ratios, roughly
17:1, 13:1 and 7:1. APCA (FRAG-PATTERTECH-HOUSE-01) argues those ratios
misdescribe perceived contrast on dark grounds. It is also not a standard and
was pulled from WCAG 3 in 2023 (FRAG-PATTERTECH-HOUSE-02). Resolution: WCAG 2.2
AA stays the binding floor because it is the only thing that can be asserted;
a perceptual check is an internal readability review, never a conformance
claim.

**Measure.** The house sets the reading column at 48rem and about 60 to 70
characters. Dyson and Haselgrove (FRAG-PATTERTECH-HOUSE-04) found best
comprehension near 55 characters, with longer lines faster to read but worse
understood. Later news-reading work reports the opposite ordering for speed and
preference. So the number is a choice about which variable is being optimised,
and the house choice is comprehension. That should be written down as a choice,
not quoted as a fact.

**Motion.** The GPU whitelist is not taste: transform and opacity are the
compositor-cheap properties (FRAG-PATTERTECH-HOUSE-07), and layer promotion has
a memory cost that has to be budgeted (FRAG-PATTERTECH-HOUSE-08). What is taste
is the dimmer setting. What is safety is the character of the motion: large
moving areas, parallax and scroll-coupled movement are the vestibular triggers
(FRAG-PATTERTECH-HOUSE-09), and honouring `prefers-reduced-motion` is not
enough on its own because most users never set it.

## Binding, default, preference

**Binding.** WCAG 2.2 AA contrast for all text and the section-furniture
hierarchy expressed as real headings (EV-0027). Content visible without
JavaScript. `prefers-reduced-motion` honoured with a global kill. Animation
restricted to transform, opacity, one-shot filters and shadow transitions on
small elements. No scroll-coupled large-area motion. Diagram positions derived
from data, no label or box overlapping a line, no glow on a line. Every shipped
image has intrinsic dimensions, a web-sized variant and lazy loading. No
horizontal scroll at 375 pixels.

**Default, overridable with a written reason.** The four light tiers and their
alpha budgets. The container decision table. Section mark anatomy, index then
hairline then kicker then title, flush left. Three type roles and three
families as the ceiling. A surface ladder of four to six steps derived in a
perceptually uniform space (FRAG-PATTERTECH-HOUSE-12). Reading measure near 55
to 70 characters. One warm interlude per piece. At most two persistent
travelling rules per page.

**Preference, ours and not portable.** Cyan as the live accent and the
Cherenkov story behind it. Amber as the authority and quote voice. The andon
line across the top of the chrome. Plate numbering as `Fig. 01` joined by a
hairline. The reticle. The specific numbers: six per cent field alpha, ten per
cent bloom, eighteen second conduit duty cycle, twelve second live rule.

## Open questions, where the evidence is thin

- **The signature motif claim.** Doctrine 7 says one motif promoted everywhere
  becomes identity. No primary evidence for this was located at the cutoff. The
  brand-distinctiveness literature that would support it sits behind commercial
  publication. Treat as a working hypothesis, not a finding.
- **The budget numbers.** Every alpha and duty-cycle figure in `LIGHT.md` is
  calibration from one project, not measurement. They are reproducible because
  they are written down, not because they are correct.
- **The generic-tell test.** Useful and unfalsifiable. It has no oracle a cold
  agent can run, which is why the drill below tests the mechanical rules and
  leaves the taste judgement to a human reviewer.
- **First impressions.** Lindgaard et al. (FRAG-PATTERTECH-HOUSE-14) show the
  judgement forms in about 50 milliseconds, which argues for spending on the
  first screen. It does not show that the judgement is correct or that it
  survives use, so it cannot justify ornament that costs comprehension.
- **Dark register cost for our actual audience.** Untested. Nobody has measured
  whether the polarity penalty matters for the readers we have.

## Refresh triggers

Cutoff 2026-08-03. Re-open when: WCAG 3 selects a visual contrast method; CSS
Color 4 or the Properties and Values API changes status; engine guidance on
compositor-only properties changes; or any house budget number is challenged by
a measurement rather than an opinion.
