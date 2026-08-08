---
summary: The error-message contract in detail, placement, timing, wording, input survival and the human against machine split
kind: fact
scope: estate
sources: [EV-0027, EV-0062, EV-0063, EV-0122, EV-0233, EV-0440, EV-0441, EV-0447]
volatility: slow
review: on-change-of:WCAG-2.2
type: ux
tags: [forms, a11y, content]
---

# Error contract

Detail behind B4, B5 and B6 in `packs/writing-content/PACK.md`. An
error message has four separable jobs, and most bad ones fail on the
first two before wording is even reached
(EV-0441).

## Placement

The message is a descendant or a sibling of the control that caused it,
and is associated programmatically so assistive technology reaches it
from the field. A summary at the top of a form is additive, never the
only location, and each summary entry moves focus to its field. The
GOV.UK error summary and error message components (EV-0062, EV-0063)
solve this structurally, which is the point: a component that cannot be
placed wrongly beats a rule a writer has to remember.

The failure this prevents: a precise, kind, well-worded message
rendered in a banner three scroll heights from the field.

## Timing

Validation that can only be decided on submit fires on submit.
Validation that can be decided per field fires when the field is
finished, not on the second keystroke. Nothing fires while the person
is still typing the first instance of a value. Success states may
appear early; failure states may not.

## Wording

Name the condition, then state the required input or the next action
(EV-0027, criteria 3.3.1 and 3.3.3). Replace a diagnosis with the shape
of a correct answer: an identifier that is not valid becomes a
statement of what a valid identifier looks like
(EV-0447). Literal language, one instruction, no idiom
and no metaphor (EV-0440). Do not blame the reader, and
do not apologise at length either: the reader wants the fix.

Severity matches consequence. A recoverable field error and a lost
payment do not get the same visual weight, and colour is never the only
signal (EV-0233).

## Input survival

After a failed submit, every value the person typed is still there.
This is the single most operational rule in the set: a message with
clumsy grammar that preserves input is better than an elegant one that
does not (EV-0441). Passwords are the usual exception
and the usual excuse; clearing every other field alongside them is the
defect.

## The human and machine split

Two artefacts, neither derived from the other by string formatting.

| Audience | Artefact | Contract |
| --- | --- | --- |
| A person | the rendered message | this file |
| A client | a problem-details body (EV-0122) | api-integration pack |

A machine `detail` field rendered to a user is a defect, and so is a
client parsing a translated interface string. The machine half carries
a stable type identifier so the client can branch; the human half
carries a message id so the translator can work. They change for
different reasons and at different rates.

## What this file does not cover

Whether the failure should have been possible at all, which is a form
design question for the ui-ux pack. What a command-line or log failure
says, which is docs-dx B5. Retry, backoff and idempotency, which are
api-integration and devops-reliability. This file is only about what a
person sees when a thing they typed was not accepted.
