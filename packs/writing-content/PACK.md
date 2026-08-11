---
summary: Writing and content, message structure and error behaviour bind, voice splits three ways, readability never gates
type: playbook
tags: [voice, content, a11y, forms]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [writes_user_facing_text, has_forms, ships_second_locale, writes_venture_documentation, writes_eos_internal_prose, reuses_external_style_guidance]
activation_paths: [**/*.md, **/locales/**, **/i18n/**, **/*.po, **/messages/**, **/*strings*.json, **/errors/**]
volatility: slow
review: on-change-of:CLDR-plural-categories
sources: [EV-0027, EV-0062, EV-0063, EV-0122, EV-0233, EV-0433, EV-0434, EV-0435, EV-0436, EV-0437, EV-0438, EV-0439, EV-0440, EV-0441, EV-0442, EV-0443, EV-0444, EV-0445, EV-0446, EV-0447, EV-0448, EV-0335]
---

# writing-content

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
ranks none of the four philosophies in GD-WRIT-001.

The seam with docs-dx on errors: docs-dx binds what a failure message
says. This pack binds where it renders, when it fires, and what happens
to the input that caused it.

## The three voice scopes

Version one of this estate applied one voice law everywhere, which was
wrong: a rule written to keep a shared brain consistent was pressed
into service as a product style guide and as a brand. ADR-0002
re-scoped it. The three are separate and they are allowed to disagree.

| Scope | Authority | What it governs | Basis |
| --- | --- | --- | --- |
| eos-internal | default, and E004 fails the build | every file in this repository | decision, ADR-0002 |
| venture | default | documentation and product copy in a venture repo | standard, plain-language guidance |
| brand:`<name>` | preference | how a venture sounds to its market | taste, adopted explicitly |

The first row read binding until the 2026-08 audit. B8 failed the basis
leg and sits under Defaults now, which changes nothing an agent does:
check E004 still fails the build on an em-dash, and `AGENTS.md` states
the same law in the file every session already reads.

A brand scope caps at preference by `kernel/METADATA_SPEC.md`, so no
brand voice can ever bind a venture's engineers. Where the scopes
conflict on a specific string, the narrower scope wins on tone and the
wider scope wins on structure: a brand may choose its own register, and
may not choose to build a sentence by concatenation. GD-WRIT-003
carries the fork.

The third row is a shape with nothing in it. No brand voice has been
written or adopted anywhere in this estate, here or in
`packs/pattertech-house/`, which covers the house look and says plainly
that it is not a copy guide. Saying so is the point: a venture is not
in breach of anything by having no brand voice, and no venture inherits
one by default.

## Binding requirements

Four bind. Each names its predicate, its evidence and the failure it
prevents, and each states its basis, because binding is the most
expensive claim this pack makes. Most of what follows this section is
default or preference, which is the correct shape for a domain where
almost every published style guide is asserted rather than tested.

The 2026-08 authority audit under ADR-0008 put one test to all ten
requirements this pack used to bind: a rule binds only where it prevents
a concrete failure that is serious or hard to reverse **and** its basis
is law, a standard, empirical evidence or a protected-set floor. B3, B5,
B6, B7, B8 and B10 failed it and are now defaults. They keep their B
numbers, because `packs/writing-content/CHECKS.md`, the guides, the refs
and the exemplar cite them, and they sit under Defaults below. A default
is departed from in writing, never in silence.

Every EV id points at a row in `registry/evidence.json`. The sixteen
sources researched for this pack were imported as EV-0433 to EV-0448,
and every citation here uses the ledger id. Each row carries its own
version, licence, access date, maintenance state and review trigger. The
frozen batch the import was made from stays at
`packs/writing-content/research/sources.fragment.json`, and the
synthesis behind the pack is in
`packs/writing-content/research/NOTES.md`. This pack cites ids,
restates none of them, and copies no source prose: several of these
sources are readable and not reusable, and which ones is recorded in
`packs/writing-content/research/provenance.fragment.json`.

**B1. No user-facing sentence is assembled by string concatenation.**
`writes_user_facing_text`. One message, one message id, with any
variation selected inside the message
(EV-0442, EV-0444). Prevents the one
localisation defect a translator cannot repair downstream, because word
order, agreement and clause structure are decided by the source code
rather than by the language. Basis: standard. Binds on the
hard-to-reverse leg: the defect is structural, it is nearly free to
avoid beforehand, and after the fact it costs a rewrite of every call
site.

**B2. Plural and gender selection resolves per locale through CLDR
categories, never from the English pair.** `ships_second_locale`. The
category `one` means "behaves like one in this language" and is not the
number one (EV-0443). Prevents a locale with four
plural forms being served two, and prevents a hardcoded switch on six
tags that is already wrong for some locales. Basis: standard. Binds for
the same reason as B1: the English pair is baked into the source, and
unpicking it is the rewrite.

**B4. Every blocking error identifies what failed and states the
required input or the next action.** `has_forms`. WCAG 2.2 success
criteria 3.3.1 and 3.3.3 make this a conformance obligation where they
apply (EV-0027). Replacing a diagnosis with the shape of a correct
answer is the highest-yield rewrite in the set
(EV-0447). Prevents `Invalid input`, which tells the
reader only that they have failed. Basis: standard. Binds because a
person who cannot tell what a good answer looks like cannot finish the
form at all, which is serious wherever the duty in 3.3.1 reaches and
wherever it does not.

**B9. Licence obligations on external style guidance are recorded
before the guidance informs a house guide.**
`reuses_external_style_guidance`. Open Government Licence material
requires attribution (EV-0435), and CC BY-NC material
cannot be adopted into a commercial product's guide at all
(EV-0448). Prevents a licensing event dressed up as a
copy-paste. Basis: law. Binds because published infringement is not
withdrawn by deleting the file afterwards.

## Defaults

Followed unless the task records a reason to depart.

### Demoted from binding, 2026-08

Six rules that used to bind. Each still names the failure it prevents,
and each says which leg of the ADR-0008 test it failed. Numbers are
unchanged so the checks, guides, refs and exemplar that cite them still
resolve.

**B3. A pseudo-locale build passes before any string reaches a
translator.** `ships_second_locale`. No truncation, no missing glyphs,
no unexternalised strings (EV-0446). Prevents paying
for the same mechanical defect in every locale at once, which is what
happens when the first real translation is also the first test.
Basis: decision, taken on vendor guidance rather than on a trial. The
source is a maintainer document last touched in 2024 with an
unverified licence, and no study of its effect was found. Failed the
basis leg, on that admission.

**B5. An error renders adjacent to its cause, does not fire before the
person has finished, and never destroys what they typed.** `has_forms`.
Placement and timing fail more often than wording
(EV-0441, EV-0233), and structural components exist
that fix placement so no writer has to remember it (EV-0062, EV-0063).
Prevents the well-written message rendered in a banner at the top of
the page, and prevents the retype. Basis: decision, on practitioner
consensus rather than a measured effect. Failed the basis leg. The part
of it that a statutory duty reaches is already carried by
`packs/ui-ux/` B3 and B4 through form labels and the keyboard contract.

**B6. Human error text and machine error bodies are separate
artefacts.** `writes_user_facing_text`. A problem-details response
(EV-0122) is for a client, not for a person, and neither is derived
from the other by string formatting. Prevents a machine `detail` field
being rendered to a user, and prevents a client parsing a translated
interface string. Basis: standard. Failed the seriousness leg here: a
badly rendered detail field is fixed in one place. Where an outside
client has started parsing the string, the lock-in is an accidental
public contract and `packs/api-integration/` owns it.

**B7. One banned-and-preferred term list runs in CI over user-facing
strings and documentation, and only one prose linter exists in the
repository.** `writes_user_facing_text`. Vale is the recorded tool
(EV-0335). Prevents two spellings of one action reaching a
translator as two concepts, and prevents the second linter that
disagrees with the first. Basis: decision, and an admittedly cheap
bet: no study was found showing that a maintained termbase improves
comprehension or reduces support load. Failed the basis leg, on that
admission.

**B8. Prose in this repository follows the voice law.**
`writes_eos_internal_prose`. Plain, spoken, British spelling, no
em-dashes, no exclamation marks, no AI cliches, no two-fragment
antithesis. Scope eos-internal only. Prevents drift in the one
repository every agent reads. Basis: decision, ADR-0002. Failed the
basis leg: a house ruling about a house is not law, a standard or a
measured effect, and no study of a voice rule's effect was looked for
or found. It does not clear the seriousness leg either, because prose
that drifts is repaired by rewriting it.

Demoting it changes nothing an agent does. Check E004 fails the build
on an em-dash and warns on exclamation marks and cliches, so the
mechanical part is not departable in this repository whatever this pack
says about its authority, and `AGENTS.md` states the same law in the
file every session reads. What a task can record a reason against is
the judgement part, the register and the phrasing. The rule still
carries no authority over a venture's product copy or its brand.

**B10. No readability formula gates a merge, a release or a review.**
`writes_user_facing_text`. A score may be reported on a diff and may
never block one. Formulas measure sentence length and syllable counts,
which sit downstream of difficulty rather than being difficulty
(EV-0436). Prevents copy being chopped into fragments
to satisfy a number while the reader learns nothing new. Basis:
decision. The study behind the doubt is narrow, and the ruling is the
estate's, not the study's. Failed the basis leg. A venture that wants
to gate on a formula now records why, which is a fair place for that
argument to happen.

### Standing defaults

- **Front-load the answer, lead with the verb, one instruction per
  step** (EV-0435, EV-0440,
  EV-0447). The three flagship guides agree here, which
  is the strongest signal available in a domain with almost no trials.
- **Literal language in anything the reader must act on.** No idiom, no
  metaphor, simple tense and voice in instructions and errors
  (EV-0440). Contractions are fine everywhere.
- **Write for the lowest literacy in the audience, not the median**
  (EV-0435). Specialists cope with plain wording.
- **Layout slack sized for two to three times expansion on strings
  under ten characters** (EV-0445). Buttons, tabs and
  labels are the shortest strings and therefore the highest risk. The
  figures cover English into European languages only.
- **Sentence case for headings and interface labels.** An arbitrary
  call, made once so nobody argues it twice.
- **A comprehension claim is tested with real readers before it is
  made** (EV-0434). The transferable design is an A/B
  of two renderings of one decision with comprehension questions as the
  outcome (EV-0438).
- **Venture documentation follows the plain-language defaults above**,
  not the EOS voice law. A venture may use em-dashes.

## Preferences

Taste. Depart freely, no reason needed.

- Report a readability score at all. B10 settles that it cannot gate;
  whether it is worth printing is taste.
- Tone varying with the reader's emotional state, celebration copy
  reading differently from a failed payment (EV-0448).
  Asserted by its author, and worth trying.
- Serial comma, spacing after a full stop, contraction density. Settled
  per scope by GD-WRIT-003 and not debated per pull request.
- Writing about people treated as a first-class section of a style
  guide rather than an appendix (EV-0448).
- A short house term list over a full termbase, until the term list is
  demonstrably not enough.

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| Which clarity philosophy governs this text | Who holds the control point, and what the acceptance test is | `packs/writing-content/guides/GD-WRIT-001-clarity-philosophy.md` |
| How a sentence is built for a second locale | Message format, migration cost, what a translator may express | `packs/writing-content/guides/GD-WRIT-002-message-structure.md` |
| Which voice applies to this text | Register, style rules, who may overrule | `packs/writing-content/guides/GD-WRIT-003-voice-scope.md` |
| How prose is checked in CI | What blocks a merge and what only reports | `packs/writing-content/guides/GD-WRIT-004-prose-gate.md` |

Detail the body defers to sits in `packs/writing-content/refs/`: the
error contract and the i18n mechanics. A worked example is in
`packs/writing-content/exemplars/EX-WRIT-001-order-panel-second-locale.md`.

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
  (EV-0442, EV-0444). GD-WRIT-002
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
