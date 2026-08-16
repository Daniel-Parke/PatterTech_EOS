---
id: WG-WRIT-002
summary: How is a user-facing sentence built so a second locale can express what English never had?
kind: wargame
type: wargame
tags: [content, eos, forms, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-WRIT-001, DOC-WRIT-002, DOC-WRIT-005]
applies_when: [writes_user_facing_text]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0442, EV-0443, EV-0444, EV-0445, EV-0446]
review: on-change-of:CLDR-plural-categories
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-WRIT-002: How is a sentence built for a second locale?

## Decision question and stakes

PACK.md B1 forbids concatenation and B2 requires per-locale plural
selection. This Wargame decides what carries them: which message format
the venture adopts, and what it costs to change later. The fork is
real because the ecosystem is not settled, and the wrong bet costs a
migration rather than a rewrite.

## Doctrines or coverage gap under pressure

- `DOC-WRIT-001` (binding): No user-facing sentence is assembled by string concatenation.
- `DOC-WRIT-002` (binding): Plural and gender selection resolves per locale through CLDR categories, never from the English pair.
- `DOC-WRIT-005` (default): A pseudo-locale build passes before any string reaches a translator.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Whether a second locale is shipped, planned, or merely imaginable.**
- **What the platform's i18n library already supports**, since a format
  with no runtime on your stack is not an option.
- **How many strings exist today.** Migration cost scales with the
  string count, not with the locale count.
- **Whether translators are professionals with tooling**, or a
  contributor pool with a text editor.
- **How long the product is expected to live.** A format that stopped
  moving in 2019 is a different risk over ten years than over two.

Applicability is `writes_user_facing_text`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. MessageFormat 2.0
Selection on plurality, gender and grammatical case lives inside the
message, and the normative text is published as part of LDML
(EV-0442). Buys a standards-process format with the
widest intended adoption, and asymmetric localisation, so a translator
adds variants the English never had without a code change. Costs a
young adoption curve: library support was still consolidating at the
2026-08 cutoff and parts of the default function set were Draft, so the
version must be pinned.

### B. Project Fluent
The same asymmetric-localisation conclusion reached years earlier with
a different syntax, and three official implementations in JavaScript,
Python and Rust (EV-0444). Buys a stable, shipped
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
Choosing D and then concatenating is the worst outcome in this Wargame.

## Failure premises

### Premortem for A. MessageFormat 2.0

Assume `A. MessageFormat 2.0` was selected and the outcome failed. Test this option's stated failure mechanism first: a young adoption curve: library support was still consolidating at the 2026-08 cutoff and parts of the default function set were Draft, so the version must be pinned.

### Premortem for B. Project Fluent

Assume `B. Project Fluent` was selected and the outcome failed. Test this option's stated failure mechanism first: a bet against the standards process: Syntax 1.0 has not moved since 2019 and its author describes the project as research.

### Premortem for C. ICU MessageFormat 1, already in place

Assume `C. ICU MessageFormat 1, already in place` was selected and the outcome failed. Test this option's stated failure mechanism first: the asymmetry: the number of variants tends to be fixed by the source, the syntax is famously hard for translators to edit safely, and it is the format both A and B were designed to replace.

### Premortem for D. Flat strings with an explicit single-locale lock

Assume `D. Flat strings with an explicit single-locale lock` was selected and the outcome failed. Test this option's stated failure mechanism first: a migration the day that decision changes, and it only stays honest if B1 is still enforced, meaning no concatenation even with one language. Choosing D and then concatenating is the worst outcome in this Wargame.

## Decision rule

If a second locale is shipped or planned within a year and the platform
has a working runtime, choose A and pin the version. If A has no
runtime on the stack but Fluent does, choose B and record it as a bet.
If a large ICU MessageFormat 1 estate already exists and no second
locale is imminent, stay on C and forbid new concatenation rather than
funding a migration nobody needs. Choose D only with a written decision
naming who may revoke it.

## Safe default

A, pinned, from the first commit that creates a string file. It is
cheapest to adopt when there are ten strings and most expensive when
there are ten thousand.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether a second locale is shipped, planned, or merely imaginable.**** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, pinned, from the first commit that creates a string file. It is cheapest to adopt when there are ten strings and most expensive when there are ten thousand.

**Exit condition:** Stop or roll back the selected branch when a young adoption curve: library support was still consolidating at the 2026-08 cutoff and parts of the default function set were Draft, so the version must be pinned, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether a second locale is shipped, planned, or merely imaginable.**

## Counter-evidence and transfer limits

### Preserved reasoning: What holds under every option

These follow the format rather than any one format's properties. B1 and
B2 in PACK.md bind; B3, the pseudo-locale build, is a default since the
2026-08 audit, so a project that skips it writes down why.

- No sentence assembled by concatenating lookups.
- Plural categories looked up per locale, never derived from the
  English singular and plural pair. The category `one` is not the
  number one (EV-0443).
- A pseudo-locale build before any string reaches a translator, which
  catches truncation, unexternalised strings and hardcoded text at no
  translation cost (EV-0446). It catches nothing about
  meaning, so passing it says nothing about whether the copy is good.
- Layout slack for two to three times expansion on short strings
  (EV-0445). That figure covers English into European
  languages and says nothing about CJK or right-to-left scripts.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
