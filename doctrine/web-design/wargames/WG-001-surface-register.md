# WG-001: Dark, light, or dual register?

status: active
review_by: 2027-07

## The question

Does the site render on a dark ground, a light ground, or both (a theme
switch or a mixed register where reading surfaces go light)?

## It depends on

- The brand's physics: does its identity involve light, glow or emission
  (favours dark), or paper, print and daylight (favours light)?
- The signature visuals: canvas glow and luminous diagrams need a dark
  ground to exist at all.
- Print siblings: if the company ships light PDFs, a light reading register
  rhymes with them; a dark site can still hold dark-native long reads with a
  tonal ladder.
- Content mix: data-dense app surfaces read well dark; very long text is
  easier to sustain light, unless the dark body contrast is engineered
  properly (~13:1).
- Maintenance budget: every register roughly doubles the token and QC
  surface. Dual is a real cost, not a toggle.

## Options

### A. Dark-first, single register
One set of tokens, glow-native visuals, needs a deliberate surface ladder so
long pages are not one flat void. Cheapest to hold consistent.

### B. Light-first, single register
Editorial print feel by default; signature glow pieces need reworking or
framing as dark islands.

### C. Dual register (theme switch)
User choice, twice the surface to design, test and QC. Only worth it when the
audience genuinely spans both contexts (e.g. an app used day and night).

### D. Mixed register (dark chrome, light reading surfaces)
The strongest "this is a document" cue for research-led sites; costs a second
register for the article kit only.

## Decision rule

If the brand's identity is luminous or the signature visuals emit light,
choose A and build the surface ladder. If the brand is print-native and the
visuals are ink-like, choose B. Choose C only with a demonstrated
dual-context audience. Consider D when long reads dominate and the print
siblings are light, and the team accepts the second register's QC cost.

## Default

A: dark-first with a formal surface ladder and a single warm interlude
surface. It keeps one register to maintain and lets glow-native signature
pieces breathe.

## Worked rulings

- **PatterTech Website (2026-07)**: chose A. The Cherenkov identity is
  emitted light, the hero and diagrams are glow-native, and the maintenance
  budget is one person. The monotone risk was answered with the surface
  ladder (void -> surface -> surface-2 -> surface-3 -> ember) and interlude
  bands rather than a light register. D was considered and declined for QC
  cost; revisit if the journal grows past ~20 long reads.
