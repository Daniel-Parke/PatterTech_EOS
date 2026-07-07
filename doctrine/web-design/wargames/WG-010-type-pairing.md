# WG-010: How to pick the type trio?

status: active
review_by: 2027-07

## The question

Which three faces (display, text, mono) does a new project take?

## It depends on

- The brand's one-word feel (precise, warm, institutional, playful) tested
  against the display face at h1 size.
- Language and glyph coverage (kanji, symbols, tabular figures).
- Licensing and delivery: self-hostable or Google-served, subsettable,
  variable axes if weights matter.
- Whether numbers are load-bearing (tabular figures in the display or mono
  face become mandatory).

## Options

Not a face list but a pairing method:

1. Choose the display face by setting the actual h1 lines in it and reading
   them aloud; if the face makes you write mottos, it is too loud.
2. Choose the text face for invisibility at the body size and measure; test
   a full article page, not a specimen.
3. Choose the mono for temperature match with the display (both geometric,
   or both grotesque) because it will sit beside it in every section mark.
4. Verify: weights needed exist, `tabular-nums` behaves, kickers read at
   0.7rem tracked, and total transfer stays inside the font budget.

## Decision rule

Follow the method; reject any trio that fails step 4 regardless of taste.
Re-use a previous project's trio only if the brands genuinely share a feel;
the trio is identity, not infrastructure.

## Default

For a technical-editorial brand with no strong pull: a geometric grotesque
display, a neutral high-x-height text face, and a matching programmer mono
(the PatterTech trio of Space Grotesk / Inter / JetBrains Mono is the proven
instance).

## Worked rulings

- **PatterTech Website (2026-07)**: kept Space Grotesk 600 / Inter /
  JetBrains Mono. The mono was promoted from code-voice to the site-wide
  annotation voice (indices, kickers, meta, captions, footer), which is what
  makes the trio earn its third member.
