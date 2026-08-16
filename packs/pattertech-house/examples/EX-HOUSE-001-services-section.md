---
summary: A services section and closing band built from the house kit, worked against the drill's ten criteria
kind: example
scope: brand:pattertech
type: example
tags: [web, layout, motion, content]
---

# EX-HOUSE-001: one section, built from the house kit

The situation. An adopting venture has an empty static skeleton and one
line of brief: build the services section of a PatterTech page, four
parallel service offerings each with a title, a line of description and
a lead time in days, then add the closing band. This is the scenario in
`packs/pattertech-house/research/DRILL_PROPOSAL.md`, worked through so
the reasoning is visible rather than the output alone.

## The decisions, in order

**1. What is this content?** Four parallel facts. Under
`packs/pattertech-house/wargames/WG-HOUSE-002-container-choice.md` that is
a ledger, not four panels. The tell that would give away a wrong answer:
if the four boxes each hold one sentence, the boxes were decoration.

**2. Where do the lead times go?** They are a meta column on the ledger
rows, in the mono annotation voice. They are not a plaque, because a
plaque is a readout of the numbers an argument turns on, and a lead time
is an attribute of a row. They are certainly not stat cards, which the
house does not have.

**3. How does the section open?** With the section mark, in the fixed
order: index, hairline, kicker, title. Flush left, as real heading
structure, with the index hanging into the rail on wide viewports.

**4. What light does it carry?** The venture ruled posture C in
`packs/pattertech-house/wargames/WG-HOUSE-001-light-posture.md`. This
section is interior reading matter, so it gets the section rule charging
once as it reveals and the ledger rows opting into bloom. It gets no
field, because the field is spent on the interlude and the home seams,
and no travelling conduit, because the viewport already has one in the
chrome.

**5. How does it close?** A colophon: hairline, mono kicker, one display
sentence, onward paths as mono text links. Not a call-to-action slab.

## The markup shape

```html
<section class="marked" aria-labelledby="s-02">
  <header class="section-mark">
    <span data-role="index" aria-hidden="true">02</span>
    <span data-role="rule" aria-hidden="true"></span>
    <span data-role="kicker">What we do</span>
    <h2 data-role="title" id="s-02">Services</h2>
  </header>

  <ol class="ledger" data-container="ledger">
    <li class="ledger-row" data-bloom>
      <span class="ledger-index">01</span>
      <h3 class="ledger-title">Systems architecture</h3>
      <p class="ledger-body">Boundaries, data topology and the
        failure modes each one buys.</p>
      <span class="ledger-meta"><span class="num">10</span> days</span>
    </li>
    <!-- three more rows, same anatomy -->
  </ol>
</section>
```

The index and the rule are decorative and hidden from assistive
technology. The kicker is text rather than an image. The heading carries
the id the section is labelled by, so the outline reads as a document.
The meta column is a span rather than a table cell, because four rows of
one attribute are not a record.

## The style shape

```css
.section-mark { text-align: left; }
.ledger-row { border-top: 1px solid var(--rule); }
.ledger-row:hover { border-top-color: var(--rule-bright); }
.ledger-meta { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }

@keyframes charge {
  0%   { transform: translateX(-101%); }
  10%  { transform: translateX(101%); }
  100% { transform: translateX(101%); }
}
@keyframes ignite { from { filter: brightness(var(--ignite-peak)); } to { filter: brightness(1); } }

.section-rule::after { animation: charge var(--conduit-duty) linear infinite; }
.reveal.is-shown { animation: ignite var(--ignite-duration) ease-out; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  [data-bloom]::after { display: none; }
}
```

Two keyframe blocks, two properties between them, both on the whitelist.
Every duration and factor arrives as a token fed from
`packs/pattertech-house/references/BUDGETS.md`, so the charge loop runs at the
resolved duty cycle rather than the older figure the v1 foundations
carried, and no number is retyped here.

The percentages in `charge` are the duty cycle, and they are the point
of the block. `packs/pattertech-house/references/LIGHT_MECHANICS.md` builds a
conduit to move during the first tenth and hold offscreen for the rest,
so the bright core is a passing event on a mostly still rule. This
exemplar used to run a plain `from`/`to` translate, which travels for
the whole period: same token, same duration, same property, and a light
that is never off screen. That is a persistent slow traveller, which
`BUDGETS.md` allows on monuments only, and criterion 8 below says this
section has no monument. A drill found it.

The reduced-motion block is a global kill rather than a per-component
opt-out, because a per-component list is a list somebody will forget to
extend.

## Worked against the drill's criteria

| # | Criterion | How this section satisfies it |
| --- | --- | --- |
| 1 | One ledger, zero panels | The four offerings are one ordered list marked as a ledger. No panel appears in the section |
| 2 | Lead times are not stat cards | The meta column carries no border and no shadow. Nothing numeric in the section has both |
| 3 | Furniture order | The header's children are index, rule, kicker, title, in that DOM order, tagged by role |
| 4 | Flush left | The section mark and every heading inherit left alignment. Nothing in the section is centred |
| 5 | Animation whitelist | Two keyframe blocks, animating transform and filter. No background-position, no geometry, no paint loop |
| 6 | Reduced motion | One global block kills animation and transition and removes the bloom layer |
| 7 | Contrast floor | Text tiers come from the ladder, measured on the ground rather than read off the token file. The floor binds from `packs/ui-ux/PACK.md` |
| 8 | No glow on reading matter | The ledger body has no text shadow. Radiance is reserved for monuments, and this section has none |
| 9 | No horizontal scroll | The ledger is width-agnostic and sits in the reading measure. Nothing sets its own maximum width |
| 10 | No script dependency | The section renders complete without scripting. Reveal hidden states sit behind a scripting query, and bloom is an enhancement |

## What a cold agent gets wrong here

The failure this exemplar exists to prevent is criterion 5. A surface
can satisfy every visible rule, look calm in a screenshot, and repaint
on every frame because somebody animated a gradient position to make the
rule travel. That is the one check a reviewer cannot make by eye, and it
is why the whitelist is written as a property list rather than as advice
about restraint.

The second commonest failure is criterion 2: the lead times arrive as
four bordered tiles with a soft shadow, because stat cards are what a
model reaches for when it sees a number beside a label. The house has no
stat card. It has a plaque for the numbers an argument turns on, and a
meta column for everything else.
