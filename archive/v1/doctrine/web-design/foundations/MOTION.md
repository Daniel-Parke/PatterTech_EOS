---
summary: Motion with meaning, reveals, easing and reduced-motion duty
type: foundation
tags: [web, motion]
status: archived
---

# Motion

What may move, and how. Doctrine 8 applies: motion means something. The
light-specific tiers live in LIGHT.md; this page is the motion budget.

## The four sanctioned kinds

1. **Live visuals.** The signature animated pieces (hero canvases, animated
   schematics, drawing charts). The project's energy budget concentrates
   here. They pause when hidden, cap device pixel ratio, and render a static
   frame under reduced motion.
2. **Ambient light.** Fields breathe over 60-120s; conduits travel on duty
   cycles of 18s or longer. Slow enough that nobody watches it happen, alive
   enough that stillness never sets in (see LIGHT.md).
3. **One-shot furniture reveals.** Section marks, figures and quotes may fade
   or rise into view once, igniting briefly as they arrive. Reading matter
   (paragraphs, lists, tables, notes) never animates in: readers are there to
   read, and a fade-up on every paragraph is the loudest template tell of all.
4. **Functional and presence-reactive feedback.** Hover, focus, progress,
   state changes, and the bloom that answers the cursor. Quiet and quick
   (0.2-0.4s), and never a transform that moves content the user is trying to
   read or click (no lifts on cards or buttons).

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
| Interlude bands, chosen seams | Field breathe (60-120s, opacity only) |
| Chrome hairlines, charged rules, progress | Conduit travel (>= 18s duty or one-shot) |
| Section furniture, figures, quotes | One-shot reveal + ignite |
| Buttons, links, rows, panels | Colour/border transitions, arrow nudge, cursor bloom |
| Paragraphs, lists, tables | None |
| Status indicators | Pulse only if genuinely live |
