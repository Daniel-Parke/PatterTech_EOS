---
summary: Venture lock-book template, the machine rulings header and the module contract sections
type: template
tags: [eos]
template: true
extracted_from: Venture A@d2e3250
eos_root: {{EOS_ROOT}}
eos_version: {{EOS_VERSION}}
eos_commit: {{EOS_COMMIT}}
scale: {{SCALE}}
stack: {{STACK_PROFILE}}
policy_profile: {{POLICY_PROFILE}}
packs_adopted: []
addons: []
compiled: {{COMPILED_DATE}}
rulings_record: docs/RULINGS.json
---

# {{VENTURE_NAME}} lock-book

The venture's contract with the EOS. This file wins on specifics; EOS
Doctrine wins on standing rules. The YAML header above is machine-read:
the seed check validates it, the harvest reads the structured Rulings
record, and upgrades diff against the pins. `policy_profile` names the
compiled policy instance; `packs_adopted` lists the knowledge packs this
venture activates, and house style activates only by adoption here.
`docs/RULINGS.json` records why each candidate Wargame was selected or
omitted and holds the argued outcomes. Inherited Doctrine is carried by
the EOS pin and adopted packs, so it is not expanded into empty rows.

## Identity

- One-word feel: {{FEEL}}
- Signature motif (promoted everywhere): {{MOTIF}}
- Signature animated pieces (the sanctioned exceptions, by name): {{SIGNATURE_PIECES}}
- Voice register: rule through `GD-WRIT-003` when its pressure engages;
  the result belongs in `docs/RULINGS.json`.

## Narrative brief

The one-paragraph story the design must tell without saying it: what
the visitor should feel, what stays concealed, what escapes anyway.
Name the physics or motifs the brand draws from and how each becomes a
mechanism, not a mood board. This paragraph informs the live house-style
Wargames `GD-HOUSE-001`, `GD-HOUSE-003` and `GD-HOUSE-004` when that pack
has been adopted.

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

Before a first build exists, a gate the stack profile does not already
name takes the same sanctioned deferral: `set at first build` plus where
the command gets ruled.

- Build: {{GATE_BUILD}}
- Overflow at 375: {{GATE_OVERFLOW}}
- Page weight: {{GATE_WEIGHT}}
- Screenshots: {{GATE_SCREENSHOTS}}
- Regression smokes: {{GATE_SMOKES}}

## Structural contracts (things future edits must not break)

- {{STRUCTURAL_CONTRACTS}}

## Deviations from doctrine

This section is a human-readable pointer only. The canonical entry is in
`docs/RULINGS.json`: the Doctrine departed from, the pressure, the Wargame
that argued it, the reason and any approval reference. If no Wargame covers
the pressure, record the gap in `docs/EOS_FEEDBACK.md` and keep the venture
Ruling local until EOS admits a reusable scenario.
