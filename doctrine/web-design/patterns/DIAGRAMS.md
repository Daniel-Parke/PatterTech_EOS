---
summary: Diagram kit rules, positions from data, labels that never overlap
type: pattern
tags: [web, media]
---

# Diagrams and charts

The diagram language is often the strongest candidate for a project's
signature motif (Doctrine 7): if the diagrams are excellent, promote their
vocabulary to the whole page. These rules keep a diagram from ever reading as
amateur. They generalise the Studio chart standard
(`PatterTech_Business/platform/docs/CHART_STYLE.md`).

## Rules

- **Positions come from data.** Scales and spread functions place every node;
  a node dot sits exactly on its datapoint. Hand-placed pixels drift and lie.
- **No label or box overlaps a line.** Offset labels at least 6px clear and
  join each to its node with a hairline connector. Arrows end at their final
  node; they never overshoot into space.
- **Small anchored boxes, restrained fills, sentence-case labels, thin
  frames.** Boxes annotate; they do not dominate.
- **No glow on a line; at most one endpoint accent.** The single allowed
  accent marks the datum that matters (semantic ornament again).
- **Two-colour semantics.** If the project has a primary and counter-accent,
  give them meanings inside diagrams (PatterTech: cyan is material/power,
  amber is authority/value) and never swap them.
- **Reflow, don't shrink.** Diagrams stack vertically on mobile rather than
  scaling into illegibility or forcing horizontal scroll. SVG charts must fit
  the column width and rely on a zoom control for detail.
- **Zoom affordance.** Dense figures carry a corner expand control opening a
  fullscreen view (Esc, backdrop, close button; scroll locked; reduced-motion
  aware). A corner button, not a whole-frame click, so interactive diagrams
  keep their own controls.
- **Animation is earned.** A diagram may animate if the motion shows the
  system working (flowing packets, a drawing line). Animated diagrams pause
  when hidden and freeze under reduced motion.

## The kit approach

Build diagrams from a tiny shared kit (scale helpers plus Spine, NodeDot,
Connector, LabelBox primitives) rather than one-off SVG. The kit enforces the
rules by construction and gives every figure the same voice. Keep the kit's
class names stable if any capture/export tooling depends on them.
