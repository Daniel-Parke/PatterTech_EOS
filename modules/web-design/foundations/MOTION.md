# Motion

What may move, and how. Doctrine 8 applies: motion means something.

## The three sanctioned kinds

1. **Live visuals.** The signature animated pieces (hero canvases, animated
   schematics, drawing charts). These are the project's energy budget and the
   only things allowed to glow or loop. They pause when hidden, cap device
   pixel ratio, and render a static frame under reduced motion.
2. **One-shot furniture reveals.** Section marks, figures and quotes may fade
   or rise into view once. Reading matter (paragraphs, lists, tables, notes)
   never animates in: readers are there to read, and a fade-up on every
   paragraph is the loudest template tell of all.
3. **Functional feedback.** Hover, focus, progress, state changes. Quiet and
   quick (0.2-0.4s), and never a transform that moves content the user is
   trying to read or click (no lifts on cards or buttons).

## Rules

- One standard easing curve per project, tokenised.
- `prefers-reduced-motion` neutralises everything, in CSS globally and in any
  JS-driven animation.
- **No-JS visibility:** if a reveal hides content before JS runs, gate the
  hidden state behind `@media (scripting: enabled)` so content is never
  invisible without JavaScript.
- Prefer CSS + IntersectionObserver for reveals over a motion library: it
  keeps server and client markup identical (no hydration drift), costs no
  bundle, and is trivially reduced-motion safe. Keep a motion library only
  for genuinely stateful animation (scroll-linked progress, orchestrated
  draw-ins).
- No autoplaying media, no parallax on reading surfaces, no scroll-jacking.

## Budget by element class

| Element | Allowed motion |
| --- | --- |
| Hero / signature visual | Continuous, within its own frame |
| Section furniture, figures, quotes | One-shot reveal |
| Buttons, links, rows | Colour/border transitions, arrow nudge |
| Paragraphs, lists, tables | None |
| Status indicators | Pulse only if genuinely live |
