---
summary: How is a user-facing sentence built so a second locale can express what English never had?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [FRAG-WRITING-CONTENT-10, FRAG-WRITING-CONTENT-11, FRAG-WRITING-CONTENT-12, FRAG-WRITING-CONTENT-13, FRAG-WRITING-CONTENT-14]
review: on-change-of:CLDR-plural-categories
type: guide
tags: [content, forms, tooling]
review_by: 2028-09
---

# GD-WRIT-002: How is a sentence built for a second locale?

## The question

PACK.md B1 forbids concatenation and B2 requires per-locale plural
selection. This guide decides what carries them: which message format
the venture adopts, and what it costs to change later. The fork is
real because the ecosystem is not settled, and the wrong bet costs a
migration rather than a rewrite.

## It depends on

- **Whether a second locale is shipped, planned, or merely imaginable.**
- **What the platform's i18n library already supports**, since a format
  with no runtime on your stack is not an option.
- **How many strings exist today.** Migration cost scales with the
  string count, not with the locale count.
- **Whether translators are professionals with tooling**, or a
  contributor pool with a text editor.
- **How long the product is expected to live.** A format that stopped
  moving in 2019 is a different risk over ten years than over two.

## Options

### A. MessageFormat 2.0
Selection on plurality, gender and grammatical case lives inside the
message, and the normative text is published as part of LDML
(FRAG-WRITING-CONTENT-10). Buys a standards-process format with the
widest intended adoption, and asymmetric localisation, so a translator
adds variants the English never had without a code change. Costs a
young adoption curve: library support was still consolidating at the
2026-08 cutoff and parts of the default function set were Draft, so the
version must be pinned.

### B. Project Fluent
The same asymmetric-localisation conclusion reached years earlier with
a different syntax, and three official implementations in JavaScript,
Python and Rust (FRAG-WRITING-CONTENT-12). Buys a stable, shipped
syntax with real production history behind it. Costs a bet against the
standards process: Syntax 1.0 has not moved since 2019 and its author
describes the project as research.

### C. ICU MessageFormat 1, already in place
The incumbent almost everywhere. Buys no migration and universal
library support. Costs the asymmetry: the number of variants tends to
be fixed by the source, the syntax is famously hard for translators to
edit safely, and it is the format both A and B were designed to
replace.

### D. Flat strings with an explicit single-locale lock
One flat string per message, no selection, and a recorded decision that
this product ships one locale. Buys the least machinery. Costs a
migration the day that decision changes, and it only stays honest if
B1 is still enforced, meaning no concatenation even with one language.
Choosing D and then concatenating is the worst outcome in this guide.

## Decision rule

If a second locale is shipped or planned within a year and the platform
has a working runtime, choose A and pin the version. If A has no
runtime on the stack but Fluent does, choose B and record it as a bet.
If a large ICU MessageFormat 1 estate already exists and no second
locale is imminent, stay on C and forbid new concatenation rather than
funding a migration nobody needs. Choose D only with a written decision
naming who may revoke it.

## Default

A, pinned, from the first commit that creates a string file. It is
cheapest to adopt when there are ten strings and most expensive when
there are ten thousand.

## Non-negotiables under every option

These hold whichever option is chosen, because they are B1, B2 and B3
in PACK.md rather than properties of a format.

- No sentence assembled by concatenating lookups.
- Plural categories looked up per locale, never derived from the
  English singular and plural pair. The category `one` is not the
  number one (FRAG-WRITING-CONTENT-11).
- A pseudo-locale build before any string reaches a translator, which
  catches truncation, unexternalised strings and hardcoded text at no
  translation cost (FRAG-WRITING-CONTENT-14). It catches nothing about
  meaning, so passing it says nothing about whether the copy is good.
- Layout slack for two to three times expansion on short strings
  (FRAG-WRITING-CONTENT-13). That figure covers English into European
  languages and says nothing about CJK or right-to-left scripts.

## Worked rulings

- **Worked example (2026-08, argued)**: A, adopted at ten strings, with
  a pseudo-locale gate added in the same change. See
  `packs/writing-content/exemplars/EX-WRIT-001-order-panel-second-locale.md`.
- **Mechanics (2026-08, inherited)**: the plural-category and expansion
  detail is in `packs/writing-content/refs/I18N_MECHANICS.md` rather
  than restated here.
