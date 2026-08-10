---
summary: Interface work, one accessibility and token spine under eight design philosophies chosen per surface
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
activation_paths: [**/components/**, **/app/**, **/pages/**, **/routes/**, **/*.tsx, **/*.jsx, **/*.svelte, **/*.vue, **/*.css, **/*.scss, **/stories/**, **/*.stories.*, **/tokens/**]
volatility: slow
review: on-change-of:WCAG-2.2
sources: [EV-0027, EV-0028, EV-0029, EV-0030, EV-0062, EV-0063, EV-0064, EV-0065, EV-0066, EV-0067, EV-0103, EV-0104, EV-0227, EV-0228, EV-0229, EV-0230, EV-0232, EV-0234, EV-0235, EV-0236, EV-0237, EV-0238, EV-0239, EV-0240, EV-0241]
type: guide
tags: [web, a11y, layout, perf]
---

# ui-ux

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

## Binding requirements

Five bind. Each names its predicate, its evidence and the failure it
prevents.

The 2026-08 authority audit under ADR-0008 put one test to all eight
requirements this pack used to bind: a rule binds only where it prevents
a concrete failure that is serious or hard to reverse **and** its basis
is law, a standard, empirical evidence or a protected-set floor. B2, B7
and B8 failed it and are now defaults. They keep their B numbers,
because `packs/ui-ux/CHECKS.md`, the guides and the refs cite them, and
they sit under Defaults below. A default is departed from in writing,
never in silence.

Every EV id points at a row in `registry/evidence.json` carrying that
source's version, licence, access date, maintenance state and review
trigger. The fifteen sources researched for this pack were imported as
EV-0227 to EV-0241, and the frozen batch the import was made from stays
at `packs/ui-ux/research/sources.fragment.json`. This pack cites ids and
never restates them, and it never copies source prose: several of the
sources below are readable and not reusable.

**B1. Conformance is stated as named criteria, not confidence.**
`has_web_ui`. A surface claiming WCAG 2.2 at a level names the level
and the criteria that pass (EV-0027). The artefact is a conformance
record listing the level, every criterion in it and that criterion's
verdict; C5 settles it, and a claim with no such record fails whatever
the scanner says. Prevents a conformance claim that rests on how the
reviewer felt. Basis: standard. Binds because the claim is a public
statement that cannot be withdrawn from the people who read it, and
where `statutory_a11y_duty` holds it is a legal one.

**B3. The six cheap failure classes are gated individually.**
`has_web_ui`. Contrast, image alternative text, form labels, empty
links, empty buttons and declared page language each get their own
assertion (EV-0235, EV-0236). Prevents the defects that the 2026 census
found on the majority of home pages shipping again here. Basis:
standard. Binds because each of the six stops somebody using the
surface at all, which is serious whether or not it is also unlawful.

**B4. Every interactive component maps to an APG pattern or documents
its deviation with a behaviour test.** `has_user_interface`. The map
names the pattern, its keys and its states (EV-0028, EV-0029).
Prevents custom widgets that render correctly and cannot be operated.
Basis: standard. Binds for the same reason as B3: a control nobody can
operate by keyboard excludes that person from the task entirely. C8
carries focus visibility, which is a WCAG criterion in its own right
(EV-0027).

**B5. No accessibility overlay, bought or hand-rolled.**
`has_web_ui`. No script that claims to repair accessibility at runtime,
and no assistive-technology sniffing (EV-0237). C12 settles it against
a written list of vendor names and runtime-patching patterns kept beside
the scan and reviewed when it changes; "no overlay" with no list behind
it is an assertion rather than a check, and a scan of built output finds
nothing it was not told to look for. Prevents a non-conforming product
being marketed as conforming, and prevents disability status being
detected without consent. Basis: decision on the overlay half, on a
consensus statement rather than a trial; law on the sniffing half,
because inferring assistive-technology use infers disability, which is
special-category personal data that `packs/security-privacy` B5 already
binds. Data protection is a protected-set item under `GOVERNANCE.md`,
and that is what kept this binding when the audit ran.

**B6. Tokens are defined once and generated; derived files are never
hand-edited.** `has_design_tokens`. One source in the DTCG shape, with
per-platform outputs produced by a build (EV-0030, EV-0065, EV-0064).
Prevents platforms drifting apart and prevents a value edited in one
output being silently overwritten. Basis: standard. Binds because
ADR-0008 keeps the derived-file rule by name: a file with a generator is
never hand-edited, and that failure has happened in this repository
twice.

## Defaults

Followed unless the task records a reason to depart.

### Demoted from binding, 2026-08

Three rules that used to bind. Each still names the failure it prevents,
and each says which leg of the ADR-0008 test it failed. Numbers are
unchanged so the checks, guides and refs that cite them still resolve.

**B2. The claim is evidenced by a real-browser run with pinned tags,
plus a written verdict on every incomplete.** `has_web_ui`. Automated
checks run in a real browser engine, rule tags pinned to WCAG 2.2 A and
AA, zero violations, and each `incomplete` result carries a human
verdict in a named file (EV-0236). Prevents a green build being read as
proof, and prevents best-practice rules being smuggled in as
conformance. Basis: decision. Failed the basis leg: the research graded
the pinned real-browser run a default and this pack promoted it, which
the Open questions section has always said. The conformance claim keeps
its evidence route regardless, because C5 is what settles B1 and C5 is
the pinned real-browser run. What became a default is the zero-violation
gate and the written verdict on every incomplete.

**B7. Every component declares its interaction states.**
`has_user_interface`. Focus, hover, active, disabled, loading and error
are named in an exported states manifest, one entry per component per
state, and C9 walks that manifest with one render assertion per entry.
A state a component cannot enter is declared absent in the manifest
with a reason rather than left out of it, because a missing entry and
a deliberate omission are indistinguishable to the walk. The full six is
an estate decision, taken because a restrained visual style removes
affordance that has to be paid back somewhere (EV-0234, EV-0232, both
weak). Basis: decision. Failed the basis leg on those two weak sources.
Focus visibility does not move with it: it is a WCAG criterion
(EV-0027) and C8 asserts it under B4.

**B8. One named philosophy per surface, recorded before pixel work.**
`has_user_interface`. The record names the philosophy from the list in
`packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md` and cites at
least one evidence id; C10 and C11 settle those two. "Before pixel
work" is settled by the record's first commit preceding the first
commit that touches the surface's styles, which is a question the
history can answer. Prevents a house style arriving by default and
prevents the estate losing the reason a surface looks as it does.
Basis: decision. Failed the basis leg, which this pack already admitted.
The pluralism contract survives the demotion: departing from a default
is itself a written act, so a house style still cannot arrive by
silence. It remains the only thing this pack says at all about how a
surface looks.

### Standing defaults

- **Headless behaviour layer plus own visual layer** (EV-0066). One
  behavioural core under many skins is what makes pluralism affordable.
- **Field performance is a design constraint on public surfaces**
  (EV-0241), with the budget written down and measured in the field,
  and any revenue claim settled by experiment rather than by citing a
  case study.
- **Assume automated accessibility coverage of roughly a third**, not
  the tool vendor's 57 per cent, when deciding what a passing build
  proves (EV-0236, EV-0104).
- **On a native platform, the system control with system behaviour is
  the starting point**, with house style applied inside it (EV-0230,
  EV-0229).
- **Honour reduced-motion preferences globally**, in CSS and in any
  script-driven animation, with a static frame for signature visuals.
  WCAG puts most of this at AAA, so it does not bind at AA; it is
  default because it costs almost nothing.
- **Content stays visible without JavaScript.** Reveal patterns hide
  content only where scripting is known to be on.
- **A dashboard commits to a method** such as RED, USE or the four
  golden signals, and orders panels to answer one named question
  (EV-0240).

## Preferences

Taste. Depart freely, no reason needed.

- A small component surface over a large one (EV-0239).
- Graded browser compatibility over binary support (EV-0062, EV-0063).
- An evidence gate before a component is admitted to a shared kit
  (EV-0103).
- Written context carried inside a dashboard rather than in a wiki
  (EV-0240).
- A reading grid with one default measure and opt-in wider bleeds, so a
  component is correct wherever it is dropped.
- One tokenised easing curve per project.

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| Which philosophy does this surface take | Density, type scale, component inventory, tone | `packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md` |
| Where do interactive components come from | Upstream fix flow, bundle, freedom to restyle | `packs/ui-ux/guides/GD-UIUX-002-component-sourcing.md` |
| How much accessibility assurance | What a passing build is allowed to claim | `packs/ui-ux/guides/GD-UIUX-003-a11y-assurance.md` |
| Where do tokens live and how do they reach platforms | Drift risk, rebrand cost, design-tool coupling | `packs/ui-ux/guides/GD-UIUX-004-token-source.md` |
| How dense, for whom | Reading aids and information per screen | WG-WEB-006 (v1, carried) |
| Motion and ornament budget | What may move and how much | WG-WEB-004, WG-WEB-005 (v1, carried) |

Reference material the body defers to sits in `packs/ui-ux/refs/`, and
a worked end-to-end example in `packs/ui-ux/exemplars/`.

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
  GD-UIUX-001 are shapes observed in maintained systems, not a tested
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
- **The 18s against 12s conduit contradiction from v1 is unresolved
  here.** The older doctrine states a duty cycle of 18 seconds or
  longer; the newer argued ruling in WG-WEB-005 relaxed it to 12. The
  newer argued ruling wins, and the resolution lands in the house
  preference pack in Wave B, not here. This pack carries no house
  motion numbers at all.
