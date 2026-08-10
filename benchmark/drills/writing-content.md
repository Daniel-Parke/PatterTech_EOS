---
summary: Cold-agent acceptance drill for the writing-content pack, make a concatenated error string survive a second locale
type: example
tags: [eos, testing]
---

# Drill proposal: writing-content pack

## Fixture

One run, one cold agent, no human turns after the prompt.
`drills/writing-content/fixture/` ships a small React and TypeScript
signup form at a fixed commit, English only, `en.json` holding flat
strings, copied to a temp directory per run. Planted defects: the
item-count message is built by concatenation from three lookups plus a
number; the password error renders as `Invalid input` in a banner above
the form rather than next to the field, and clears the typed value on
failure; the submit button is a fixed 96px box around the label `Save`;
the string `Try again` is hardcoded in JSX and never passed through
`t()`; `en.json` uses both `sign in` and `log in` for one action. No
pseudo-locale, and no lint over strings.

## Prompt given to the agent

"Read the writing-content pack. This form ships in a second language
next quarter and it is failing accessibility review today. Fix it and
make this class of failure impossible to reintroduce silently."

## Machine-checkable criteria, grader runs the final tree, all must pass

1. No source line matches a translation lookup followed by string
   concatenation, and the item count resolves through one message id
   with in-message plural selection.
2. A pseudo-locale exists. Rendering the form under it at 360px yields
   no element whose `scrollWidth` exceeds its `clientWidth`.
3. Under the pseudo-locale the DOM contains no literal `Try again`.
   This is the hardcoded-string oracle.
4. Adding a locale file with the four Polish plural categories renders
   the correct form for n of 1, 2, 5 and 22 with no change under `src/`.
5. The password error is a descendant or sibling of the password input,
   wired by `aria-describedby`, states the requirement with a digit or
   the word `characters`, and is not `Invalid input`.
6. After a failed submit, both input values are unchanged.
7. A CI step checks terminology over `en.json`, passes on the final
   tree, and fails when the grader injects `log in`.
8. No readability score gates any step. A forty-word sentence injected
   into `en.json` must not fail anything on its own.
9. At least one commit, nothing under `drills/` modified, under twenty
   minutes, and criteria 1 to 8 run with no network.

## Scoring and freeze

Pass requires all nine. Criteria 1 to 4 test that i18n was fixed
structurally rather than by rewording, 5 and 6 the error rules
including WCAG 3.3.3, 7 terminology as a check rather than a habit, 8
that the agent knew which signals must never block. Fixture hash,
injected strings, Polish locale, viewport width and grader are frozen
before any pack content is authored, so the pack cannot be written
to the drill.
