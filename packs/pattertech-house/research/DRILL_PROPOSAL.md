---
summary: Single-run cold-agent acceptance drill for the PatterTech house style, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# DRILL-HOUSE-001: one section, built from the house kit

## Scenario

A cold agent is given the pattertech-house pack and an empty static site
skeleton containing only `index.html`, `tokens.css` and a Playwright
runner. The prompt is one line: "Build the services section of a
PatterTech page. Four parallel service offerings, each with a title, a
one-line description and a lead time in days. Then add the closing band."

Single run, no follow-up prompts. Content is fixed by the fixture at
`fixtures/services.json`. Pass requires all ten criteria; each is a
static parse of the built CSS and HTML or a Playwright assertion.

## Criteria

1. **Container choice.** The four offerings render as a ruled list: the
   built HTML contains exactly one element with `data-container="ledger"`
   and zero elements with `data-container="panel"` inside that section.
   Four parallel facts must not become four boxes.
2. **Lead times are a plaque or a ledger meta column, not stat cards.**
   No element carrying a numeric value has both a four-sided border and
   a `box-shadow` in computed style.
3. **Section furniture order.** Inside the section header, the DOM order
   of children matches `index`, `rule`, `kicker`, `title`. Assert by
   `data-role` attributes, exact sequence.
4. **Flush left.** Computed `text-align` of the section header and of
   every heading in the section is `left` or `start`. Zero `center`.
5. **Animation whitelist.** Parse every `@keyframes` block in the built
   CSS. The set of animated properties is a subset of
   `{opacity, transform, filter, box-shadow, text-shadow,
   background-position}`, and any `background-position` keyframe block is
   referenced by exactly one rule whose `animation-iteration-count` is
   `1`. Any other property fails.
6. **Reduced motion.** A `@media (prefers-reduced-motion: reduce)` block
   exists and, under emulation, every element returns computed
   `animation-play-state: paused` or `animation-name: none`.
7. **Contrast floor.** For every text node in the section, the computed
   foreground and its resolved background give a WCAG 2 ratio of at least
   4.5:1, and body-tier text at least 7:1. Computed by script from
   rendered colours, not from the token file.
8. **No glow on reading matter.** Every element whose computed
   `font-size` is at or below `1.1rem` and whose text is longer than
   forty characters has computed `text-shadow: none`.
9. **No horizontal scroll.** At viewport widths 375, 768 and 1280,
   `document.documentElement.scrollWidth <= window.innerWidth`.
10. **No script dependency.** With JavaScript disabled, the section's
    text content is byte-identical to the enabled run.

## Scoring

Ten of ten passes. Anything less fails, and the failing criterion names
the guide that was not followed. Criterion 5 is load-bearing: it is the
only check that catches a plausible surface built from per-frame
repaints.
