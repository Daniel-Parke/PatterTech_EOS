---
summary: Activation, outcomes and decision map for the ui-ux Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [has_user_interface]
activation_paths: [**/components/**, **/app/**, **/pages/**, **/routes/**, **/*.tsx, **/*.jsx, **/*.svelte, **/*.vue, **/*.css, **/*.scss, **/stories/**, **/*.stories.*, **/tokens/**]
volatility: slow
review: none
sources: [EV-0027, EV-0028, EV-0029, EV-0030, EV-0062, EV-0063, EV-0064, EV-0065, EV-0066, EV-0067, EV-0103, EV-0104, EV-0227, EV-0228, EV-0229, EV-0230, EV-0232, EV-0234, EV-0235, EV-0236, EV-0237, EV-0238, EV-0239, EV-0240, EV-0241]
type: pack
tags: [web, a11y, layout, perf]
display_name: Interface Design and Accessibility
category: experience-content
id_namespace: UIUX
depends_on: [product-discovery]
---


# Interface Design and Accessibility

This pack covers interface work: what an interface must achieve for the
people using it, and how to choose a design philosophy for a surface
rather than inherit one. It activates on any task that designs, builds
or reviews a user interface, web or native. Accessibility, keyboard
behaviour and token discipline bind where they apply. Visual style,
density, component architecture and performance do not, and the
philosophy behind a surface is chosen per surface and recorded.

## Activation

**Paths.** Anything under a surface, app, web, ui, components, pages,
routes, styles, design-system, tokens or storybook directory; token
source and generated token outputs; stylesheet and template files;
component test and story files.

**Task types.** Design a surface or flow; build or change a component;
restyle or rebrand; accessibility work or remediation; interface
review; design-system creation, adoption or migration; dashboard or
report layout; front-end performance work.

**Keywords, fallback only.** Interface, screen, page, layout, design
system, component, token, accessible, WCAG, contrast, focus, keyboard,
screen reader, responsive, dashboard, form, dark mode.

**Applicability predicates.** Requirements below name the predicate
that turns them on. The pack defines these:

| Predicate | True when |
| --- | --- |
| has_user_interface | anything a person looks at or operates |
| has_web_ui | the surface renders in a browser engine |
| has_native_ui | the surface ships as an iOS, Android or desktop app |
| is_public_surface | reachable by people outside the venture |
| has_forms | the surface takes input and can reject it |
| has_shared_components | two or more surfaces share a component |
| has_design_tokens | values are named once and consumed by name |
| statutory_a11y_duty | a public-sector, procurement or legal duty applies |

A surface with no web UI does not inherit the web requirements. It
activates its platform profile instead, and the platform's own
conformance route applies.

## Outcomes and non-goals

**Outcomes.** People can complete the task the surface exists for,
including by keyboard and with assistive technology. A conformance
claim is backed by named criteria that pass. Two surfaces in one estate
can look and behave differently on purpose without duplicating
behaviour code or token sources. The philosophy behind a surface is
written down, so the next person argues with a decision instead of
guessing at taste.

**Non-goals.** This pack does not pick a look. It carries no house
palette, type stack, component kit or section furniture. It does not
rank the philosophies. It is not a brand system, a content strategy, a
copy guide, or an analytics or experimentation practice. Where a
venture wants PatterTech house style, that is a separate preference
pack it adopts explicitly, and adoption is a recorded choice.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-UIUX-001](doctrines/DOC-UIUX-001-conformance-is-stated-as-named-criteria-not-confidence.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-UIUX-002](doctrines/DOC-UIUX-002-the-six-cheap-failure-classes-are-gated-individually.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-UIUX-003](doctrines/DOC-UIUX-003-every-interactive-component-maps-to-an-apg-pattern-or.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-UIUX-004](doctrines/DOC-UIUX-004-do-not-add-a-script-that-claims-to-repair-accessibility-at.md) (default), [DOC-UIUX-005](doctrines/DOC-UIUX-005-do-not-infer-assistive-technology-use-without-the-persons.md) (binding)
<a id="B6"></a>
- `B6` to [DOC-UIUX-006](doctrines/DOC-UIUX-006-tokens-are-defined-once-and-generated-derived-files-are.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-UIUX-007](doctrines/DOC-UIUX-007-the-claim-is-evidenced-by-a-real-browser-run-with-pinned.md) (default)
<a id="B7"></a>
- `B7` to [DOC-UIUX-008](doctrines/DOC-UIUX-008-every-component-declares-its-interaction-states.md) (default)
<a id="B8"></a>
- `B8` to [DOC-UIUX-009](doctrines/DOC-UIUX-009-one-named-philosophy-per-surface-recorded-before-pixel-work.md) (default)
- source `defaults:004` to [DOC-UIUX-010](doctrines/DOC-UIUX-010-headless-behaviour-layer-plus-own-visual-layer.md) (default)
- source `defaults:005` to [DOC-UIUX-011](doctrines/DOC-UIUX-011-field-performance-is-a-design-constraint-on-public-surfaces.md) (default)
- source `defaults:006` to [DOC-UIUX-012](doctrines/DOC-UIUX-012-assume-automated-accessibility-coverage-of-roughly-a-third.md) (default)
- source `defaults:007` to [DOC-UIUX-013](doctrines/DOC-UIUX-013-on-a-native-platform-the-system-control-with-system.md) (default)
- source `defaults:008` to [DOC-UIUX-014](doctrines/DOC-UIUX-014-honour-reduced-motion-preferences-globally.md) (default)
- source `defaults:009` to [DOC-UIUX-015](doctrines/DOC-UIUX-015-content-stays-visible-without-javascript.md) (default)
- source `defaults:010` to [DOC-UIUX-016](doctrines/DOC-UIUX-016-a-dashboard-commits-to-a-method.md) (default)
- source `preferences:001` to [DOC-UIUX-017](doctrines/DOC-UIUX-017-a-small-component-surface-over-a-large-one-ev-0239.md) (preference)
- source `preferences:002` to [DOC-UIUX-018](doctrines/DOC-UIUX-018-graded-browser-compatibility-over-binary-support-ev-0062-ev.md) (preference)
- source `preferences:003` to [DOC-UIUX-019](doctrines/DOC-UIUX-019-an-evidence-gate-before-a-component-is-admitted-to-a-shared.md) (preference)
- source `preferences:004` to [DOC-UIUX-020](doctrines/DOC-UIUX-020-written-context-carried-inside-a-dashboard-rather-than-in-a.md) (preference)
- source `preferences:005` to [DOC-UIUX-021](doctrines/DOC-UIUX-021-a-reading-grid-with-one-default-measure-and-opt-in-wider.md) (preference)
- source `preferences:006` to [DOC-UIUX-022](doctrines/DOC-UIUX-022-one-tokenised-easing-curve-per-project.md) (preference)

### Later evidence-led admissions

These records were admitted after the frozen source migration.
Their own metadata is canonical; this map does not restate it.

- [DOC-UIUX-023](doctrines/DOC-UIUX-023-native-semantics-before-custom-interaction.md) (default Doctrine)
- [WG-UIUX-001](wargames/WG-UIUX-001-web-delivery-shape.md) (Wargame)
- [WG-UIUX-002](wargames/WG-UIUX-002-semantic-or-custom-interaction.md) (Wargame)

## Decision map

| Fork | What it decides | Wargame |
| --- | --- | --- |
| Which philosophy does this surface take | Density, type scale, component inventory, tone | `packs/ui-ux/wargames/WG-UIUX-003-design-philosophy.md` |
| Where do interactive components come from | Upstream fix flow, bundle, freedom to restyle | `packs/ui-ux/wargames/WG-UIUX-004-component-sourcing.md` |
| How much accessibility assurance | What a passing build is allowed to claim | `packs/ui-ux/wargames/WG-UIUX-005-a11y-assurance.md` |
| Where do tokens live and how do they reach platforms | Drift risk, rebrand cost, design-tool coupling | `packs/ui-ux/wargames/WG-UIUX-006-token-source.md` |

Density is not a separate fork here. It falls out of the philosophy, so
WG-UIUX-003 settles it and `packs/ui-ux/references/LAYOUT_AND_MEASURE.md`
carries the structure. Motion and ornament budgets are house taste and
belong to whichever preference pack a venture adopts, which for us is
`packs/pattertech-house/references/BUDGETS.md`.

Level-three detail sits in `packs/ui-ux/references/`: the accessibility
floor, the component contract, layout and measure, performance and
motion, and the token pipeline. A worked end-to-end example is in
`packs/ui-ux/examples/`.

## Failure modes and anti-patterns

- **One house style over every surface.** A service form and an
  operations dashboard have different readers under different pressure.
  If both come out looking the same, the philosophy was never chosen.
- **The green build fallacy.** Zero automated violations with an empty
  manual verdict file. The tool says so itself (EV-0236).
- **Overlay procurement.** Buying a script instead of fixing the
  components (EV-0237).
- **Hand-edited generated tokens.** The next build reverts them and
  nobody notices for a month.
- **Keyboard tests that assert rendering.** A test that mounts a
  component and checks it appears proves nothing about keys.
- **Aesthetic adoption without the machinery.** Copying the look of a
  public-service system without its evidence gate yields a plain site
  with no discipline behind it.
- **Enterprise density in a first-run consumer flow**, which reads as
  bureaucracy, and its mirror, expressive styling on destructive or
  irreversible controls.
- **The metric wall.** Every available series on one dashboard. Common
  in the wild, defended in no published guidance (EV-0240).
- **App components reused for long-form reading**, giving a short
  measure and app-grade line height to an article.
- **Citing case-study percentages as causal.** The source that lists
  them says only an experiment measures the effect (EV-0241).

## Open questions and counter-evidence

- **No philosophy is known to outperform another.** The eight in
  WG-UIUX-003 are shapes observed in maintained systems, not a tested
  taxonomy. Fit conditions are argued, not measured.
- **Expressive against restrained is a standoff of weak evidence.**
  A vendor programme reports large gains from emphasis (EV-0232);
  an eleven-year-old opinion piece argues stripping signifiers costs
  discoverability (EV-0234). Both are weak, they point the same way
  from opposite directions, and neither should be quoted as fact. Both
  are scoped to their own surfaces and populations.
- **Automated coverage is disputed**: about 57 per cent from the tool
  maintainer (EV-0236), about a third in commonly repeated docs
  (EV-0104). The pack plans against the lower figure.
- **Distribution is genuinely contested.** Depend on a versioned system
  (EV-0227, EV-0228) or copy the source and own it (EV-0067). Team size
  and patch appetite decide, and vendoring forfeits upstream
  accessibility fixes.
- **Migration is contested too.** One large estate carries three
  component generations at once (EV-0228); another archived its React
  implementation outright and moved to web components (EV-0238). Both
  are defensible.
- **Two requirements were promoted above their research grade, and the
  audit returned them.** The research graded the real-browser
  pinned-tag run and the philosophy record as defaults; this pack bound
  them as B2 and B8 until 2026-08. The arguments for the promotion were
  that a conformance claim with no evidence route is not a claim, and
  that the pluralism contract is unauditable if the choice is not
  written down. Both arguments survive as defaults with reasons
  attached, and both are open to being argued back up the ladder.
- **Apple's guidance could not be read from the primary page**
  (EV-0230); the principle rests on secondary summaries and should be
  re-verified before it is quoted.
- **Licence is not a class rule.** One openly published system is
  restricted to apps integrating with its vendor (EV-0238). Check each
  source before reuse; five of the twenty-seven this pack cites carry a
  copyright notice and no reuse licence, and three more are unknown.
  The per-source list is in
  `packs/ui-ux/research/provenance.fragment.json`.
- **EN 301 549 v4.x and WCAG 2.2** are expected to meet in 2026 by
  several secondary sources. No primary source confirmed it, so this
  pack records nothing about it.
