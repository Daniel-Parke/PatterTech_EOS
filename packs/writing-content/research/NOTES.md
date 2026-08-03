---
summary: Research synthesis for the writing-content pack, four philosophies of clear text, what is machine-checkable, and what should bind
type: example
tags: [eos, testing]
---

# Writing and content pack research notes

Cutoff 2026-08-03. Sixteen new sources in `sources.fragment.json`, plus
existing ledger records cited by EV id. The domain question is not "how
do we write well". It is: which writing decisions can be made once and
enforced by a machine, which have to be made per reader and tested, and
which are taste that should never be allowed to block a merge.

## Four philosophies, and when each fits

They differ on where the control point sits: the writer, the word, the
reader, or the message data structure.

**1. Plain language, control at the writer.** ISO 24495-1
(FRAG-WRITING-CONTENT-01) defines plainness by reader outcome: the
intended readers can find, understand and use the thing. GOV.UK
(FRAG-WRITING-CONTENT-03) and the US federal guidelines
(FRAG-WRITING-CONTENT-02) are the two mature implementations, both
free to read, both with an attribution obligation. Fits: anything a
non-specialist reads once, under stress, to make a decision. The
strongest transferable rules are front-load the answer, use the words
the reader already uses, and write for the lowest literacy in the
audience rather than the median. Anti-pattern: adopting a reading-age
number as an acceptance criterion. Trade-off: plain language is a
skill, so it degrades whenever the writer is rushed or is a subject
expert, and nothing in the guidance detects that degradation.

**2. Controlled language, control at the word.** ASD-STE100 Issue 9
(FRAG-WRITING-CONTENT-05) removes the writer's choice: roughly
fifty-three rules and about nine hundred approved words, each word
constrained to one meaning. The claim is that ambiguity is best
attacked at the vocabulary layer, because one word with two meanings
defeats any amount of sentence discipline. Fits: procedural
instructions where a misread step hurts someone, and readers who do
not have English as a first language. Anti-pattern: applying it to
explanation or persuasion, where the resulting text is correct and
unreadable. Trade-off: it needs a maintained termbase and a linter,
which is real ongoing cost. Note that a full termbase is not necessary
to get most of the benefit; a small banned-and-preferred list enforced
in CI gets the one-word-one-meaning property for the terms that
actually matter.

**3. Content design, control at the reader.** The user need comes
first and the page exists only to serve it, which is GOV.UK's real
contribution (FRAG-WRITING-CONTENT-03) and the reason its guidance
separates principles from an A to Z of arbitrary lexical calls. In
interfaces this becomes microcopy discipline: NN/g
(FRAG-WRITING-CONTENT-09) shows most bad error messages fail on
placement and timing before wording, and the Microsoft rule
(FRAG-WRITING-CONTENT-15) of replacing a diagnosis with the shape of
the correct input is the single highest-yield rewrite we found.
Already in the ledger and load-bearing here: EV-0027 (WCAG 3.3.1 error
identification and 3.3.3 error suggestion make some of this a
conformance obligation, not a preference), EV-0062 and EV-0063 (the
GOV.UK error summary and error message components, which fix placement
structurally so no writer has to remember it), EV-0233 (heuristic 9,
the ancestor of all of this) and EV-0122 (RFC 9457, which is the
machine-readable half of the same error, and must not be confused with
the human half). Anti-pattern: writing a beautiful error string and
rendering it at the top of a page away from the field, or firing it
before the user has stopped typing.

**4. Message data, control at the structure.** MessageFormat 2.0
(FRAG-WRITING-CONTENT-10) and Project Fluent
(FRAG-WRITING-CONTENT-12) converge on asymmetric localisation: a
translation need not have the shape of its source, and the source
language must not cap what a translator can express. CLDR plural rules
(FRAG-WRITING-CONTENT-11) supply the concrete trap, that the category
`one` means "behaves like one in this language" and is not the number
one. Fits: any product that will ever have a second locale. The
decision rule that generalises even to single-locale products is: never
build a sentence by concatenation. Concatenation is the one i18n defect
no translator can repair downstream. Anti-pattern: pluralising by
appending an s, and sizing a button to its English label.

## The disagreements

**Plain language improves understanding, or only satisfaction.** This
is the load-bearing contradiction. Two randomised trials from the same
programme, same intervention type, same content domain, differ:
parents showed both preference and understanding gains
(FRAG-WRITING-CONTENT-06), youths aged fifteen to twenty-four showed
higher usability and satisfaction but no significant understanding
gain, mean difference 5.2 per cent, 95 per cent CI minus 1.2 to 11.6
(FRAG-WRITING-CONTENT-07). The honest reading is that plain language
reliably buys experience and only sometimes buys comprehension, and
that the gain shrinks as baseline literacy rises. ISO 24495-1 makes
understanding definitional, so on its own definition the youth trial is
a partial failure of the intervention. Consequence for us: we may
assert that plain wording improves the reading experience. We may not
assert a comprehension gain for a specific audience without measuring
it on that audience.

**Literal language against conversational voice.** W3C COGA
(FRAG-WRITING-CONTENT-08) says use literal language, simple tense and
voice, one instruction per step, no idiom. Microsoft
(FRAG-WRITING-CONTENT-15) says write like you speak, use contractions,
project friendliness. Mailchimp (FRAG-WRITING-CONTENT-16) goes further
with tone varying by the reader's emotional state. These genuinely
conflict. Our resolution: literal language wins in instructions,
errors, and anything a user must act on correctly; conversational voice
is allowed in confirmations, empty states and marketing. Contractions
are safe in both; idiom and metaphor are not.

**Readability formulas.** GOV.UK's reading-age target implies a
formula, and Begeny and Greene (FRAG-WRITING-CONTENT-04) show formulas
track measured difficulty only patchily and only at some bands, because
they measure surface proxies that are downstream of difficulty. A
formula score can be improved by chopping sentences without changing
what anyone understands. Formulas stay as a signal, never as a gate.

## Binding, default, preference

Binding, and machine-checkable:

- No user-facing sentence assembled by string concatenation. One
  message, one message id, variants selected inside the message.
- Plural and gender selection resolved per locale via CLDR categories,
  never derived from English.
- A pseudo-locale build passes with no truncation, no missing glyphs
  and no unexternalised strings before any string reaches a translator
  (FRAG-WRITING-CONTENT-14).
- Every blocking error message states the required input or the next
  action, is rendered adjacent to its cause, and preserves what the
  user typed. WCAG 3.3.1 and 3.3.3 (EV-0027) make part of this a
  conformance obligation.
- A banned-and-preferred term list runs in CI over user-facing strings
  and documentation. Vale is the obvious tool and is already recorded
  in the docs-dx fragment as FRAG-DOCS-DX-14; do not add a second
  prose linter.
- Attribution recorded wherever OGL or CC BY-NC material informed a
  house guide, and no NonCommercial text copied into a commercial
  product's guide.

Default, overridable with a written reason:

- Front-load the answer; lead with the verb; one instruction per step.
- Sentence case for headings and UI labels.
- Layout slack sized for a two to three times expansion on strings
  under ten characters (FRAG-WRITING-CONTENT-13).
- Literal language in anything the reader must act on.

Preference, never a merge blocker:

- Readability scores. Report them, do not gate on them.
- Serial comma, spacing, contraction density. The house voice law in
  `CLAUDE.md` settles these and it already disagrees with Microsoft on
  em-dashes; that is fine and needs no further debate.

## Open questions, where evidence is thin

- No source located measures whether a house style guide changes any
  user outcome. Every style guide here is asserted, including the two
  from large vendors. We should assume style guides buy consistency and
  reviewer speed, not comprehension.
- Terminology management is the weakest-evidenced area in this pack. We
  found tooling and standards practice but no study showing that a
  maintained termbase improves comprehension or reduces support load.
  Treat the small banned-list rule as a cheap bet, not a proven one.
- Empty states and onboarding copy have no evidence base we could find
  at all, only practitioner opinion.
- COGA has not been republished since 2021 while WCAG moved to 2.2, so
  the cognitive-accessibility guidance we rely on is drifting. Refresh
  trigger: any W3C republication of `coga-usable` or a WCAG 3 draft
  containing a plain-language success criterion.
- Two of the three plain-language flagships moved host during the last
  eighteen months, plainlanguage.gov to digital.gov and GOV.UK content
  design to the publishing guidance site. Any deep link into either is
  a maintenance liability; cite the section, keep the link shallow.
