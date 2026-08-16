---
summary: Activation, outcomes and decision map for the writing-content Doctrine and Wargames
type: pack
tags: [voice, content, a11y, forms]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [writes_user_facing_text, has_forms, ships_second_locale, writes_venture_documentation, writes_eos_internal_prose, reuses_external_style_guidance]
activation_paths: [**/*.md, **/locales/**, **/i18n/**, **/*.po, **/messages/**, **/*strings*.json, **/errors/**]
volatility: slow
review: none
sources: [EV-0027, EV-0062, EV-0063, EV-0122, EV-0233, EV-0433, EV-0434, EV-0435, EV-0436, EV-0437, EV-0438, EV-0439, EV-0440, EV-0441, EV-0442, EV-0443, EV-0444, EV-0445, EV-0446, EV-0447, EV-0448, EV-0335]
display_name: Content Design and Writing
category: experience-content
id_namespace: WRIT
depends_on: [product-discovery]
---


# Content Design and Writing

This pack covers text people read: interface strings, error messages,
product documentation and the prose in this repository. It activates on
any task that writes or reviews user-facing copy, documentation, or a
translatable string. Message structure, error identification and
licence obligations bind. Voice splits three ways: a house rule inside
the EOS that a check enforces, a default for venture documentation, a
preference for brand that nothing yet fills. Readability scores never
gate anything.

## Activation

**Paths.** Locale and message files in any format, string tables and
resource bundles, anything under a copy, content, locales, i18n, l10n
or translations tree, the templates that render user-visible text, form
and validation components, style guides and terminology lists, prose
linter configuration, and every Markdown file in this repository.

**Task types.** Write or change user-facing copy. Add, reword or move
an error message. Add a locale, or prepare for one. Write or revise
product documentation. Write or revise a house style guide or a brand
voice. Review a change whose acceptance depends on someone reading
something and getting it right.

**Keywords, fallback only.** Copy, microcopy, wording, tone, voice,
style guide, error message, validation message, empty state, plural,
translation, localisation, i18n, terminology, readability, plain
language. Keywords are the weakest signal and never override the
predicates.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| writes_user_facing_text | a person outside the team will read the string |
| has_forms | the surface takes input and can reject it |
| ships_second_locale | a second language is shipped, or is planned |
| writes_venture_documentation | prose lands in a venture repo for its own readers |
| writes_eos_internal_prose | the file lives in this repository |
| reuses_external_style_guidance | an outside guide informs a house guide |

A single-locale product with no second locale planned does not inherit
the message-structure requirements as a build gate. It still inherits
B1, because concatenation is the one defect that cannot be repaired
later, and repairing it costs the same whether the second locale ever
arrives or not.

## Outcomes and non-goals

**Outcomes.** A reader can find the thing, understand it, and act on it
(EV-0433). A translator can express in their language a
distinction the English source never had. A rejected form tells the
person what a good answer looks like and keeps what they typed. The
same product sounds like itself in three different places without one
voice rule being applied where it does not belong. A claim that copy is
clearer than what it replaced is either measured or not made.

**Non-goals.** This pack defines the brand voice scope and carries no
brand voice of its own. Nor does anything else: no adoptable PatterTech
brand voice exists in this tree. `packs/pattertech-house/` is the house
visual language and its own non-goals say it is not a copy guide, so it
does not fill the scope either. A venture that wants a brand voice
writes one and adopts it by name; until it does, nothing is missing
from it. This pack does not own link integrity, snippet execution or
generated reference, which sit in the docs-dx pack. It does not own
form layout, focus behaviour or component structure, which sit in
ui-ux. It does not own API error contracts, which sit in
api-integration. It sets no reading-age target, ships no word list, and
ranks none of the four philosophies in WG-WRIT-001.

The seam with docs-dx on errors: docs-dx binds what a failure message
says. This pack binds where it renders, when it fires, and what happens
to the input that caused it.

## Voice scopes

Voice is deliberately scoped rather than inherited as one universal law.

- EOS-internal prose resolves through [DOC-WRIT-009](doctrines/DOC-WRIT-009-prose-in-this-repository-follows-the-voice-law.md).
- Venture documentation resolves through [DOC-WRIT-017](doctrines/DOC-WRIT-017-venture-documentation-follows-the-plain-language-defaults.md).
- Brand voice remains explanatory and empty until a venture adopts a
  named brand voice. Adoption creates a brand-scoped preference; absence
  is not a breach.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

- source `voice-scope:001` to [DOC-WRIT-009](doctrines/DOC-WRIT-009-prose-in-this-repository-follows-the-voice-law.md) (default)
- source `voice-scope:002` to [DOC-WRIT-017](doctrines/DOC-WRIT-017-venture-documentation-follows-the-plain-language-defaults.md) (default)
- source `voice-scope:003` remains explanatory at [voice scopes](#voice-scopes) until a named brand voice is adopted.
<a id="B1"></a>
- `B1` to [DOC-WRIT-001](doctrines/DOC-WRIT-001-no-user-facing-sentence-is-assembled-by-string.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-WRIT-002](doctrines/DOC-WRIT-002-plural-and-gender-selection-resolves-per-locale-through.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-WRIT-003](doctrines/DOC-WRIT-003-every-blocking-error-identifies-what-failed-and-states-the.md) (binding)
<a id="B9"></a>
- `B9` to [DOC-WRIT-004](doctrines/DOC-WRIT-004-licence-obligations-on-external-style-guidance-are-recorded.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-WRIT-005](doctrines/DOC-WRIT-005-a-pseudo-locale-build-passes-before-any-string-reaches-a.md) (default)
<a id="B5"></a>
- `B5` to [DOC-WRIT-006](doctrines/DOC-WRIT-006-an-error-renders-adjacent-to-its-cause-does-not-fire-before.md) (default)
<a id="B6"></a>
- `B6` to [DOC-WRIT-007](doctrines/DOC-WRIT-007-human-error-text-and-machine-error-bodies-are-separate.md) (default)
<a id="B7"></a>
- `B7` to [DOC-WRIT-008](doctrines/DOC-WRIT-008-one-banned-and-preferred-term-list-runs-in-ci-over-user.md) (default)
<a id="B8"></a>
- `B8` to [DOC-WRIT-009](doctrines/DOC-WRIT-009-prose-in-this-repository-follows-the-voice-law.md) (default)
<a id="B10"></a>
- `B10` to [DOC-WRIT-010](doctrines/DOC-WRIT-010-no-readability-formula-gates-a-merge-a-release-or-a-review.md) (default)
- source `defaults:007` to [DOC-WRIT-011](doctrines/DOC-WRIT-011-front-load-the-answer-lead-with-the-verb-one-instruction.md) (default)
- source `defaults:008` to [DOC-WRIT-012](doctrines/DOC-WRIT-012-literal-language-in-anything-the-reader-must-act-on.md) (default)
- source `defaults:009` to [DOC-WRIT-013](doctrines/DOC-WRIT-013-write-for-the-lowest-literacy-in-the-audience-not-the.md) (default)
- source `defaults:010` to [DOC-WRIT-014](doctrines/DOC-WRIT-014-layout-slack-sized-for-two-to-three-times-expansion-on.md) (default)
- source `defaults:011` to [DOC-WRIT-015](doctrines/DOC-WRIT-015-sentence-case-for-headings-and-interface-labels.md) (default)
- source `defaults:012` to [DOC-WRIT-016](doctrines/DOC-WRIT-016-a-comprehension-claim-is-tested-with-real-readers-before-it.md) (default)
- source `defaults:013` to [DOC-WRIT-017](doctrines/DOC-WRIT-017-venture-documentation-follows-the-plain-language-defaults.md) (default)
- source `preferences:001` to [DOC-WRIT-018](doctrines/DOC-WRIT-018-report-a-readability-score-at-all.md) (preference)
- source `preferences:002` to [DOC-WRIT-019](doctrines/DOC-WRIT-019-tone-varying-with-the-readers-emotional-state-celebration.md) (preference)
- source `preferences:003` to [DOC-WRIT-020](doctrines/DOC-WRIT-020-serial-comma-spacing-after-a-full-stop-contraction-density.md) (preference)
- source `preferences:004` to [DOC-WRIT-021](doctrines/DOC-WRIT-021-writing-about-people-treated-as-a-first-class-section-of-a.md) (preference)
- source `preferences:005` to [DOC-WRIT-022](doctrines/DOC-WRIT-022-a-short-house-term-list-over-a-full-termbase-until-the-term.md) (preference)

## Decision map

| Fork | What it decides | Wargame |
| --- | --- | --- |
| Which clarity philosophy governs this text | Who holds the control point, and what the acceptance test is | `packs/writing-content/wargames/WG-WRIT-001-clarity-philosophy.md` |
| How a sentence is built for a second locale | Message format, migration cost, what a translator may express | `packs/writing-content/wargames/WG-WRIT-002-message-structure.md` |
| Which voice applies to this text | Register, style rules, who may overrule | `packs/writing-content/wargames/WG-WRIT-003-voice-scope.md` |
| How prose is checked in CI | What blocks a merge and what only reports | `packs/writing-content/wargames/WG-WRIT-004-prose-gate.md` |

Detail the body defers to sits in `packs/writing-content/references/`: the
error contract and the i18n mechanics. A worked example is in
`packs/writing-content/examples/EX-WRIT-001-order-panel-second-locale.md`.

## Failure modes and anti-patterns

- **One voice law everywhere.** The version one failure this pack
  exists to correct. A rule about a shared brain applied to a market.
- **The reading-age gate.** A formula score adopted as an acceptance
  criterion. It can be satisfied by chopping sentences without changing
  what anyone understands (EV-0436).
- **The plainness claim.** Asserting that a rewrite improved
  comprehension because it reads more easily. One trial found the gain,
  one did not (EV-0438, EV-0439).
- **Pluralising by appending an s**, and its cousin, sizing a button to
  its English label.
- **The beautiful banner.** A precise, kind, well-worded error rendered
  at the top of the page, three scroll heights from the field that
  caused it.
- **The eager validator.** An error fired on the second keystroke of an
  email address, before anyone could have finished typing.
- **Controlled language applied to explanation.** Simplified Technical
  English on a marketing page produces text that is correct and
  unreadable (EV-0437).
- **Two prose linters.** The second one disagrees with the first, and
  the team learns to ignore both.
- **The wholesale lift.** An outside A to Z copied into a house guide,
  which is a licensing event whatever the intent (B9).
- **Terminology drift in the string file.** Two words for one action,
  which reaches a translator as two concepts and comes back as two
  concepts in every locale.

## Open questions and counter-evidence

- **The load-bearing contradiction.** Two randomised trials from one
  programme, same intervention type, same content domain, disagree.
  Parents showed preference and understanding gains
  (EV-0438). Youths aged fifteen to twenty-four showed
  higher usability and satisfaction and no significant understanding
  gain, mean difference 5.2 per cent, 95 per cent confidence interval
  minus 1.2 to 11.6 (EV-0439). Both populations were
  self-selected, online, English-speaking, reading pandemic health
  advice, and the null came from a group with high baseline literacy.
  Neither result transfers to an interface string read in two seconds.
  The honest reading: plain wording reliably buys reading experience
  and only sometimes buys comprehension, and ISO 24495-1 makes
  comprehension definitional, so on its own definition the youth trial
  is a partial failure of the intervention.
- **Literal against conversational is a real conflict.** W3C COGA says
  literal language, no idiom (EV-0440). Microsoft says
  write like you speak (EV-0447), and Mailchimp goes
  further (EV-0448). This pack resolves it by surface
  rather than by ranking the sources, and that resolution is a ruling,
  not a finding.
- **Readability formulas are weak, and the study is narrow.** Begeny
  and Greene tested eight formulas against oral reading fluency in 360
  United States elementary-aged children reading aloud
  (EV-0436). That population is not an adult scanning
  an interface, and oral fluency is not comprehension. The same study
  found some formulas fair at some grade bands, so formulas are
  unreliable rather than uninformative. B10 rested on the estate's
  ruling rather than on this study, which is why the audit made it a
  default. Nothing here bans a formula from a report.
- **No source measures whether a house style guide changes any user
  outcome.** Every style guide cited here is asserted, both large
  vendors included. Assume a style guide buys consistency and reviewer
  speed, and claim nothing else for it.
- **Terminology management is the weakest area in this pack.** Tooling
  and standards practice exist. Evidence that a termbase improves
  comprehension or reduces support load does not. B7 was a cheap bet
  and is now a default, which is the honest authority for a bet.
- **Empty states and onboarding copy have no evidence base at all**,
  only practitioner opinion. This pack carries no rule about them.
- **COGA is drifting and non-normative.** Not republished since 2021
  while WCAG moved to 2.2, so it can never be cited as a legal
  obligation. Refresh trigger: a W3C republication, or a WCAG 3 draft
  carrying a plain-language success criterion.
- **The message-format ecosystem is not settled.** MessageFormat 2.0
  and Fluent reached the same conclusion by different routes, parts of
  the MessageFormat default function set were still Draft at the
  cutoff, and Fluent has not moved since 2019
  (EV-0442, EV-0444). WG-WRIT-002
  carries the bet.
- **Two flagship sources moved host in the last eighteen months**
  (EV-0434, EV-0435). Cite the section,
  keep the link shallow.
- **B1 is promoted above its research grade.** The research graded
  concatenation on two converging design documents and no trial. It
  binds anyway, because the defect is unrepairable after the fact and
  nearly free to avoid before it. Basis decision would be equally
  defensible, and the requirement is open to challenge on that ground.
  The 2026-08 audit left it binding on the hard-to-reverse leg rather
  than on the strength of the sources.
- **No brand voice exists to test any of this against.** The third
  voice scope is defined and empty, here and everywhere else in the
  tree. Nothing in this pack has ever been exercised against a real
  brand, so the conflict rule between scopes is reasoning rather than
  experience.
