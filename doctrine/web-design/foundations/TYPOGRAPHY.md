# Typography

How to derive a project's type system. Doctrine 4 applies: typography carries
the design.

## Principles

- **Three roles, three faces.** Display (headings, standfirsts), text (body,
  UI), mono (the annotation voice: indices, kickers, meta, captions, tabular
  data, footer detail). The mono face is not code decoration; it is the voice
  of precision that separates an editorial-technical site from a template.
- **Scale contrast is the cheapest oomph.** Big display steps against a calm
  body size beat any decorative treatment. If a page feels flat, widen the
  scale contrast before adding anything.
- **Reading measure ~60-70ch.** Body text lives in a measured column
  (PatterTech: 48rem at 1.05rem). Leading scales inversely with size: body
  ~1.7-1.75, display ~1.05-1.15.
- **Weights are few.** One weight for display (600 works), regular plus one
  emphasis for text. Every extra weight is a cost in load and coherence.
- **Kickers are mono, small, tracked.** ~0.7rem, uppercase, letter-spacing
  0.2-0.3em, in the accent or dim tier. This is the label voice used
  everywhere: sections, figures, colophons, tabs.

## Deriving for a new brand

1. Pick the trio: a display face with character (test it against the brand's
   one-word feel), a text face that disappears (high x-height, tight but
   generous), a mono with matching temperature. Pairing guidance: share either
   a foundry, an era or a geometry; never share all three roles in one face.
2. Set the body size first (1.0-1.1rem), then the measure, then a display
   ladder with real contrast (h1 3-4.5rem desktop stepping to ~2.25rem
   mobile).
3. Define the kicker style once as a utility; everything labelled uses it.
4. Load fonts with `display: swap` and subset where possible; three families
   is the ceiling.

## Pitfalls

- Tracked uppercase in the text face (use the mono for labels).
- Balancing every heading but not standfirsts (`text-balance` belongs on
  short display lines, not paragraphs).
- Letting UI components restate sizes instead of consuming the scale.
- Drop caps and ornament faces: almost always off-doctrine; wargame it if a
  project truly wants one.
