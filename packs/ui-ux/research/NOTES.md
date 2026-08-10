---
summary: Research synthesis for the ui-ux pack, eight design philosophies, accessibility conformance, tokens and component contracts
type: example
tags: [eos]
---

# ui-ux research synthesis (cutoff 2026-08-03)

Purpose: give the pack a design pluralism contract. The pack must be
able to produce eight materially different interfaces without smuggling
one house style in as the default, while holding one non-negotiable
accessibility and token spine underneath all eight.

## The spine that does not vary

Three things are invariant across every philosophy below.

1. Conformance is stated as testable criteria, not taste. WCAG 2.2
   (EV-0027) is a set of individually testable statements in tiers, and
   criteria get retired when they stop earning their keep. That is the
   model the pack copies: a claim of AA means named criteria pass, not
   that a designer felt confident.
2. Behaviour is a contract separate from looks. The ARIA APG (EV-0028,
   EV-0029) defines each pattern as expected keyboard behaviour plus
   roles and states, independent of any visual system, and declares
   itself non-prescriptive. Radix (EV-0066) is the same idea shipped as
   code: hard correctness for free, zero visual opinion. This is what
   makes pluralism affordable, one behavioural core, eight skins.
3. Tokens are a single source with generated derivations. Style
   Dictionary (EV-0065) and the DTCG format (EV-0030) between them give
   define-once, alias, transform per platform, and never hand-edit the
   outputs. USWDS (EV-0064) adds the sharper rule: consumers reach
   tokens through functions and one settings layer, so the structure is
   invariant while the palette is not.

## The eight philosophies and when each fits

**Content-first public service.** GOV.UK (EV-0062, EV-0063, EV-0103).
Fits when the user has no choice about using you, the task is a form or
a decision, and failure is exclusion. Signature moves: guidance in a
separate repo from code, graded browser compatibility instead of binary
support, and an evidence gate before a component is admitted.
Trade-off: slow, and it needs a standing team. Anti-pattern: adopting
the aesthetic without the evidence gate, which yields a grey site with
no discipline behind it.

**Dense enterprise.** Carbon (FRAG-UIUX-01), Fluent (FRAG-UIUX-02,
FRAG-UIUX-03). Fits internal tools, long sessions, expert users, many
apps that must feel like one. Signature moves: one versioned monorepo
carrying tokens, components, icons and grid; explicit support for
gradual multi-generation migration. Trade-off: heavy surface, slow
change. Anti-pattern: importing enterprise density into a first-run
consumer flow, where it reads as bureaucracy.

**Consumer and lifestyle.** Fits discretionary use where the user can
leave in one tap. The decision-relevant evidence is Google's expressive
research (FRAG-UIUX-06): emphasis through size, shape, containment and
colour reportedly sped target-finding up to fourfold and closed the age
gap, with strongest preference among 18 to 24 year olds. Trade-off:
unfamiliarity dampens the gain, and the same research found that
breaking established patterns hurt. Anti-pattern: expressive styling
applied to destructive or irreversible controls.

**Editorial.** Guardian Source (FRAG-UIUX-13). Fits reading, not tasks.
Signature moves: small component surface, typography and measure as the
system's centre, article furniture as first-class, and the page budget
shared with consent and analytics code. Trade-off: little governance
machinery, so it does not scale to a large multi-team estate.
Anti-pattern: reusing an app component library for long-form reading
and ending up with 60-character measure and app-grade line height.

**Conversion-led landing.** web.dev business impact (FRAG-UIUX-15).
Fits paid acquisition and commerce entry points, where a money number
is attached to the surface. Signature moves: one primary action, field
performance as a design constraint, and claims settled by experiment.
Trade-off: pressure toward dark patterns and toward optimising a local
metric. Anti-pattern: citing case-study percentages as if they were
causal, which the source itself disclaims.

**Data-heavy dashboards.** Grafana (FRAG-UIUX-14). Fits monitoring and
analysis where the reader is under time pressure. Signature moves:
commit to a method such as RED, USE or the four golden signals; order
panels as a narrative answering one named question; carry written
context in the dashboard itself. Trade-off: an opinionated dashboard
serves fewer questions. Anti-pattern: the metric wall, every available
series displayed, which is common in the wild and defended nowhere.

**Mobile-native interaction.** Apple HIG (FRAG-UIUX-04), Material
(FRAG-UIUX-05, FRAG-UIUX-06). Fits anything shipping into a platform
with its own conventions. Signature move: the system control with
system behaviour is the default, and house style is applied inside it.
Trade-off: two platforms means two truths, and a shared house language
will lose arguments to each platform's conventions. Anti-pattern:
shipping one web-styled control set to both stores and calling it
consistency.

**Minimal versus expressive.** This is an axis, not a system. The
minimal case is discipline and speed; the expressive case is that
emphasis is functional. NN/g's flat design piece (FRAG-UIUX-08) argues
stripping signifiers costs discoverability. Rule the pack should carry:
whatever is removed visually must be paid back by an explicit
interaction-state contract, focus, hover, active, disabled, loading,
error, stated per component.

## Disagreements worth recording

- **Distribution.** Carbon and Fluent say depend on a versioned system;
  shadcn/ui (EV-0067) says copy the source and own it. Team size and
  patch appetite decide. Vendoring forfeits upstream accessibility
  fixes, which is the load-bearing cost.
- **Migration.** Fluent carries three generations at once; Shopify
  archived Polaris React (FRAG-UIUX-12) and pivoted to web components.
  Both are defensible for large estates and they contradict each other.
- **Expressive versus restrained.** Google's 46-study programme and
  NN/g's opinion piece reach compatible conclusions from opposite
  directions, and both are weak evidence, vendor-run and unreviewed on
  one side, anecdotal and eleven years old on the other. Neither should
  be cited as fact.
- **Automated accessibility coverage.** axe-core's maintainer claims
  about 57 per cent of WCAG issues found automatically (FRAG-UIUX-10);
  Storybook's docs (EV-0104) repeat the commonly cited figure of about
  a third. The pack should assume the lower number when deciding what a
  green build proves.
- **Licence is not a class rule.** Polaris looks open and is restricted
  to Shopify-integrating apps. Carbon, Style Dictionary and Guardian
  Source are permissive. Apple, Fluent 2 guidance and NN/g are readable
  but not reusable. Check each source.

## Binding, default, preference

**Binding.** WCAG 2.2 AA stated as named criteria; every interactive
component maps to an APG pattern or documents its deviation with a test;
tokens defined once in DTCG shape and generated, derived files never
hand-edited; the six WebAIM failure classes (FRAG-UIUX-09) gated in CI,
contrast, alt text, form labels, empty links, empty buttons, page
language; no accessibility overlay, ever (FRAG-UIUX-11); every
component declares its interaction states.

**Default.** Headless behaviour layer plus own visual layer; one named
philosophy chosen per surface and recorded before any pixel work; field
performance budget on public surfaces; automated a11y checks run in a
real browser with rule tags pinned to WCAG, treating axe incomplete
results as a required human verdict.

**Preference.** Small component surface over a large one; graded
compatibility over binary support; an evidence gate before admitting a
new shared component; written context inside dashboards.

## Refresh triggers

New WebAIM Million edition; WCAG or APG revision; DTCG reaching a
stable spec release; a Carbon, Fluent or axe-core major; Apple or
Android OS generation; EN 301 549 v4.x incorporating WCAG 2.2, which
several secondary sources expect in 2026 and which this research could
not confirm from a primary source, so it stays unrecorded until ETSI is
readable.
