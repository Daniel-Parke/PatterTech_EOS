---
id: GD-MKTG-004
summary: Who owns a published page, and how fast may a venture publish?
kind: wargame
type: wargame
tags: [content, eos, seo, voice, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-MKTG-009]
applies_when: [publishes_public_content]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0095, EV-0353, EV-0354, EV-0356]
review: on-change-of:Google-spam-policies-revision
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-MKTG-004: Who owns a published page and why does it exist?

## Decision question and stakes

An agent can write a hundred pages in an afternoon. The index operator
does not test how text was produced; it tests why the page exists
(EV-0354). PACK.md D6 requires a named owner and a stated purpose
per page. This guide decides how much provenance machinery a venture
needs and what publishing rate that machinery supports.

## Doctrines or coverage gap under pressure

- `DOC-MKTG-009` (default): Every published page has a named human owner and a stated purpose.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Whether a real reader is identifiable** for each page, by name of
  need rather than by keyword.
- **Who answers for the page** when it is wrong.
- **Whether the page would exist if search did not.** If not, it is
  ranking bait and the policy names it.
- **How much automation went in**, since the guidance asks that
  substantial automation be evident to the visitor (EV-0356).
- **Whether the venture publishes third-party content on its domain**,
  which is where site reputation abuse lives (EV-0354).

Applicability is `publishes_public_content`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Manifest with a named owner and a one-line purpose per page
A machine-readable file listing every published page with its human
owner and why it exists, validated against the actual page set so
neither can drift. Buys a check a script runs, and a person to ask.
Costs a file that must be updated in the same commit as the page.

### B. Front-matter provenance on each page
Owner, purpose and automation disclosure carried in the page's own
metadata, with the manifest derived from it. Buys locality: the fact
travels with the artefact and cannot be forgotten separately. Costs a
generator and the habit of never editing the derived file.

### C. Editorial review before publication, no artefact
A person reads everything before it ships. Buys judgement, which is the
thing the questionnaire actually asks for. Costs the one resource a
small venture does not have, and it leaves no evidence afterwards that a
check happened.

### D. Publish freely, prune on measured failure
Ship at volume and remove what performs badly. Buys speed. Costs the
exact thing the spam policy names: scaled content abuse is defined by
purpose, and a page published to see whether it ranks has declared its
purpose. This option is excluded, and it is listed so the argument
against it is on the record rather than assumed.

## Failure premises

### Premortem for A. Manifest with a named owner and a one-line purpose per page

Assume `A. Manifest with a named owner and a one-line purpose per page` was selected and the outcome failed. Test this option's stated failure mechanism first: a file that must be updated in the same commit as the page.

### Premortem for B. Front-matter provenance on each page

Assume `B. Front-matter provenance on each page` was selected and the outcome failed. Test this option's stated failure mechanism first: a generator and the habit of never editing the derived file.

### Premortem for C. Editorial review before publication, no artefact

Assume `C. Editorial review before publication, no artefact` was selected and the outcome failed. Test this option's stated failure mechanism first: the one resource a small venture does not have, and it leaves no evidence afterwards that a check happened.

### Premortem for D. Publish freely, prune on measured failure

Assume `D. Publish freely, prune on measured failure` was selected and the outcome failed. Test this option's stated failure mechanism first: the exact thing the spam policy names: scaled content abuse is defined by purpose, and a page published to see whether it ranks has declared its purpose. This option is excluded, and it is listed so the argument against it is on the record rather than assumed.

## Decision rule

If pages number in the tens, run A: it is one file and one test. If
pages number in the hundreds or several people write them, run B and
derive A from it. Run C beside either where the subject carries real
consequence for a reader, never instead of them. Never D. Publishing
rate then follows from ownership: the rate a venture can sustain is the
rate at which it can name an owner and a reader, and no faster.

## Safe default

A. It satisfies D6 with a single artefact and a single check, and it
upgrades into B without changing what is asserted. The manifest is
checked by a test that fails on a page missing from it and on a manifest
entry with no page, so the two sets are identical by construction.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether a real reader is identifiable** for each page, by name of need rather than by keyword.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. It satisfies D6 with a single artefact and a single check, and it upgrades into B without changing what is asserted. The manifest is checked by a test that fails on a page missing from it and on a manifest entry with no page, so the two sets are identical by construction.

**Exit condition:** Stop or roll back the selected branch when a file that must be updated in the same commit as the page, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether a real reader is identifiable** for each page, by name of need rather than by keyword.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
