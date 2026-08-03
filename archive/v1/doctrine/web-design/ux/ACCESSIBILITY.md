---
summary: The accessibility floor, skip link to reduced motion
type: ux
tags: [web, a11y]
status: archived
---

# Accessibility

The floor, not a feature. These ship on every project.

- **Skip link** as the first focusable element, targeting `<main id="main">`;
  visually hidden until focused.
- **Landmarks**: one `main`, `header`, `footer`, `nav` with labels where
  duplicated.
- **Focus visible everywhere**: a global `:focus-visible` outline in the
  accent, never removed without a better replacement. Custom controls
  (carousel arrows and dots, filter tabs, zoom and audio buttons, whole-row
  links) are buttons or anchors, in the natural tab order, with real labels.
- **Contrast tiers measured** (see COLOR.md): body at ~13:1 on dark grounds,
  captions clearing AA. Record the ratios in the lock-in.
- **Reduced motion honoured** in CSS globally and in every JS animation;
  signature visuals render a static frame.
- **No-JS visibility**: reveal patterns hide content only under
  `@media (scripting: enabled)`; a reader without JavaScript gets the whole
  page, unanimated.
- **Zoom never disabled**; correct viewport meta.
- **Alt discipline**: figures describe what the figure shows; decorative
  marks are `aria-hidden`; icon-only buttons carry `aria-label`.
- **Carousels**: `role="group"` with a roledescription, per-slide position
  labels, keyboard arrows, and a text counter (not colour alone).
- **Anchored headings** carry ids and scroll margins so in-page navigation
  lands cleanly under a fixed header.
