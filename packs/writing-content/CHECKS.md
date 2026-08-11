---
summary: What a reviewer or a script can verify about writing and content work, split into executable today and judgement
kind: fact
scope: estate
sources: [EV-0027, EV-0062, EV-0122, EV-0436, EV-0441, EV-0443, EV-0445, EV-0446]
volatility: slow
review: on-change-of:CLDR-plural-categories
type: implementation
tags: [content, forms, testing]
---

# CHECKS

Evaluation criteria for work in this domain. Each row says what is
verified, against which requirement, and whether a machine can settle
it today. "Executable" means a script decides it with no human reading
the output. "Judgement" means a person rules and the record is the
evidence. A check that needs a person is still a check.

B1, B2, B4 and B9 bind. B3, B5, B6, B7, B8 and B10 are defaults since
the ADR-0008 audit, so the rows behind them still run and a project
that departs records why. C16 is the odd one: B8 is a default and
check E004 fails the commit anyway, because the voice law is this
repository's own and does not wait on the pack's authority.

## Executable today

| # | Check | Verifies | How |
| --- | --- | --- | --- |
| C1 | No source line matches a message lookup followed by string concatenation or template joining | B1 | source scan over the render layer, with a written allowlist |
| C2 | Every count or quantity message resolves through one message id with selection inside the message | B1, B2 | message-file scan, fail on a key whose value has no selector where the code passes a number |
| C3 | Adding a locale file with four plural categories renders the correct form for 1, 2, 5 and 22 with no change under the source tree | B2 | fixture locale plus a render assertion per number |
| C4 | Plural categories come from the locale data, not from a hardcoded list of tags | B2 | source scan for literal category tag switches |
| C5 | A pseudo-locale build exists and the product renders under it | B3 | build target present, run in CI |
| C6 | Under the pseudo-locale, no element's scroll width exceeds its client width at the narrowest supported viewport | B3, expansion default | headless browser walk over changed routes |
| C7 | Under the pseudo-locale, no untransformed source-language literal appears in the DOM | B3 | DOM scan, the hardcoded-string oracle |
| C8 | Every blocking error is associated with its control programmatically | B5 | markup assertion per form, association attribute resolves to the input |
| C9 | Error text is not a bare rejection: it names a requirement or a next action | B4 | assertion per error string against a banned-phrase list and a required-token rule |
| C10 | After a failed submit, every non-secret input value is unchanged | B5 | form test, compare values before and after |
| C11 | No validation message renders before the field is finished | B5 | form test, type a partial value and assert no error node |
| C12 | Rendered error text is never taken from a machine error body field | B6 | source scan for the problem-details fields reaching the render layer |
| C13 | A terminology check runs over user-facing strings and documentation, blocking | B7 | CI step present and non-advisory |
| C14 | The terminology check actually fails when a banned term is injected | B7 | mutation of the string file, assert non-zero exit |
| C15 | Exactly one prose linter configuration exists in the repository | B7 | configuration file count |
| C16 | No em-dash in any file in this repository | B8 | check E004 |
| C17 | No readability score is computed in a blocking step | B10 | CI configuration scan, and a long-sentence injection that must fail nothing |
| C18 | Every message id referenced in code exists in the source-language file, and every id in the file is referenced | B1 | two-way reference check |

C3 and C7 are the two that catch a rewording pretending to be a fix.
Renaming strings satisfies neither, which is why both are here rather
than one general "i18n is done" assertion. C14 exists because a check
nobody has watched fail is a check nobody has tested.

C6 needs a real browser engine: overflow depends on computed layout and
does not exist in a simulated DOM.

## Judgement, recorded not automated

| # | Check | What good looks like | Against |
| --- | --- | --- | --- |
| J1 | The philosophy for this body of text is named and recorded | One of the four in GD-WRIT-001, with a reason tied to reader and consequence, written before the copy | GD-WRIT-001 |
| J2 | The message format decision is recorded with its version pinned and its risk stated | A named format, a pinned version, and a sentence on what happens if the ecosystem moves | GD-WRIT-002 |
| J3 | The voice scope is correct for the file | Repository decides EOS-internal against venture; brand applies only where adopted; literal register overrides on anything the reader must act on | GD-WRIT-003 |
| J4 | Error wording states the shape of a correct answer rather than a diagnosis | A reader who has never seen the field can produce a valid value from the message alone | B4 |
| J5 | Error severity matches consequence, and colour is not the only signal | A recoverable field error and an irreversible failure look different | ERROR_CONTRACT |
| J6 | Terminology list covers the terms that matter and no more | Every entry traceable to a real drift or a real ambiguity, not a style opinion | B7 |
| J7 | Licence obligations on external guidance are recorded before use | Attribution present for OGL material, and no NonCommercial text inside a commercial guide | B9 |
| J8 | Any claim that copy is clearer is either measured or absent | A comprehension test with a real sample, or no claim | Counter-evidence in PACK.md |
| J9 | The pack's own text was not written to its acceptance drill | Rules traceable to evidence rows rather than to grader criteria | PACK_SHAPE |

J8 is the check most likely to be skipped and the one this pack cares
about most. Two randomised trials of the same intervention type
disagree on whether plain wording improves understanding, so the
default position is that it improves the reading experience and nothing
more until someone measures otherwise on the actual audience.

J9 cannot be automated and belongs to the reviewer who did not author
the pack.

## Not checked here

Link integrity, snippet execution and generated reference sit in the
docs-dx pack. Focus order, contrast and component structure sit in
ui-ux. API error contracts sit in api-integration. None of them are
weaker for living elsewhere, and duplicating them here would give two
homes to one rule.
