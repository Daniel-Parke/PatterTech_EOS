---
summary: Venture lock-book template, the machine rulings header and the module contract sections
type: template
tags: [eos]
template: true
extracted_from: Venture A@d2e3250
supersedes: the v0.1 PROJECT_LOCKIN migration
eos_root: {{EOS_ROOT}}
eos_version: {{EOS_VERSION}}
eos_commit: {{EOS_COMMIT}}
scale: {{SCALE}}
stack: {{STACK_PROFILE}}
addons: []
compiled: {{COMPILED_DATE}}
rulings:
  - WG-EOS-001 · {{SCALE}} · argued · the scale ruling, triggers engaged at Session 0
---

# {{VENTURE_NAME}} lock-book

The venture's contract with the EOS. This file wins on specifics; EOS
doctrine wins on principles. The YAML header above is machine-read: the
seed check validates it, the harvest counts its rulings, upgrades diff
against its pins. Rulings rows are one line each,
`WG-ID · ruling · argued|inherited · note`; argued means the triggers
were engaged afresh, inherited means the default was taken without new
argument. Only argued rulings are promotion evidence.

## Identity

- One-word feel: {{FEEL}}
- Signature motif (promoted everywhere): {{MOTIF}}
- Signature animated pieces (the sanctioned exceptions, by name): {{SIGNATURE_PIECES}}
- Voice register ruling (WG-VOX-001): in the header; banned list per
  the voice module.

## Narrative brief

The one-paragraph story the design must tell without saying it: what
the visitor should feel, what stays concealed, what escapes anyway.
Name the physics or motifs the brand draws from and how each becomes a
mechanism, not a mood board. This paragraph drives the light budget
(WG-WEB-005), the reactivity ruling (WG-WEB-011) and the imagery ruling
(WG-WEB-012).

{{NARRATIVE}}

## Tokens

Before a first build exists, design-system slots below take the
sanctioned deferral: `set at first build` plus where the value gets
ruled. The first-build lock-in session replaces every deferral in one
sitting and notes it in the worklog or queue.

- Token home: {{TOKEN_HOME}} · Code mirror: {{TOKEN_MIRROR}} ·
  Styleguide route: {{STYLEGUIDE_ROUTE}}
- Surface ladder: {{SURFACE_LADDER}}
- Accents: {{ACCENTS}}
- Text tiers and measured contrast: {{TEXT_TIERS}}
- Measures: reading {{MEASURE_READING}} · wide {{MEASURE_WIDE}} · full
  {{MEASURE_FULL}} · block gap {{BLOCK_GAP}}

## QC gates (exact commands)

- Build: {{GATE_BUILD}}
- Overflow at 375: {{GATE_OVERFLOW}}
- Page weight: {{GATE_WEIGHT}}
- Screenshots: {{GATE_SCREENSHOTS}}
- Regression smokes: {{GATE_SMOKES}}

## Structural contracts (things future edits must not break)

- {{STRUCTURAL_CONTRACTS}}

## Deviations from doctrine

None, or one entry each: the doctrine deviated from, the trigger that
justifies it, the wargame that argued it (a draft wargame in
docs/EOS_FEEDBACK.md if none exists), and the operator's approval.
Deviations are harvested as contrary rulings.
