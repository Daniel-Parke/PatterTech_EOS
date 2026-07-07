# QC gates

A page ships when the gates say so (Doctrine 9). Every gate is a script or a
written check; none is a vibe. Projects list their exact commands in the
lock-in.

## The gates

1. **Build**: lint, unit tests and the production build all pass. Lint
   includes the project's design lint where one exists (WG-WEB-013): the
   machine-checked half of the width and media laws, with pragma escapes
   that each carry a written reason.
2. **Overflow**: no horizontal page scroll at 375px, verified by script (a
   headless browser reporting `scrollWidth === clientWidth` and zero
   uncontained offenders), on every changed route.
3. **Styleguide acceptance**: tokens and primitives land on the styleguide
   page first and get eyes there before any real page consumes them.
4. **Measure, don't eyeball**: margins and indices aligned, nothing wider
   than its measure, diagrams free of box-on-line overlap; verified with a
   screenshot tool and element inspection, not by squinting.
5. **Page weight**: image transfer inside budget (ux/PERFORMANCE.md),
   measured by script after a full-page scroll.
6. **Regression smokes**: anything with export/capture tooling gets one
   smoke run after CSS or class changes.
7. **Voice**: read every new line of copy aloud; if it sounds like an AI
   wrote it, rewrite it before shipping.
8. **Accessibility spot pass**: keyboard through new interactive components;
   skip link, focus rings and reduced-motion behaviour intact.

## Cadence

Gates 1-2 run on every change set; 3-8 on any change that touches what they
cover. Migrations run phase by phase with the build green at every phase (see
AGENT_WORKFLOW.md).
