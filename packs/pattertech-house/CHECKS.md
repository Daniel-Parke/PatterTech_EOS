---
summary: What a reviewer or a script can verify about house work, split into executable today and judgement
kind: guide
authority: preference
basis: decision
evidence_grade: not-applicable
scope: brand:pattertech
sources: [EV-0027, EV-0236]
review: 2028-11
type: guide
tags: [web, testing, tooling, a11y]
---

# House checks

Evaluation criteria for work in an adopting venture. Each row says what
is verified, which house requirement or guide it answers to, and whether
a machine can settle it today. "Executable" means a script decides it
without a person reading the output. "Judgement" means a person rules
and the record is the evidence.

Two scoping notes before the tables. First, none of these gate anything
outside an adopting venture: this pack is preference, so a check that
fails is a conversation rather than a block. Second, the accessibility
and performance checks that genuinely bind are in
`packs/ui-ux/CHECKS.md`. The rows below that touch the same ground are
here because house output puts pressure on them, not because this pack
owns them.

## Executable today

| # | Check | Verifies | How |
| --- | --- | --- | --- |
| C1 | Exactly one ledger and zero panels in a section presenting parallel facts | H1 | parse built markup for container roles within the section |
| C2 | No numeric element carries both a four-sided border and a box shadow | H1 | computed style scan over elements containing a numeric value |
| C3 | Section header children appear in the order index, rule, kicker, title | H2 | DOM order assertion on role attributes |
| C4 | Section marks and headings compute to a left or start alignment, zero centred | H2 | computed style over the section |
| C5 | Every animated property is on the whitelist | H3 | parse each keyframes block in the built stylesheet, assert the property set is a subset |
| C6 | Any one-shot exception is referenced by exactly one rule with a single iteration | H3 | cross-reference keyframe names against iteration counts |
| C7 | A reduced-motion block exists and neutralises every animation under emulation | H4 | headless run with the preference emulated, assert paused or none on every element |
| C8 | No scroll-coupled or viewport-scale animation is declared | H4 | scan for scroll-driven timelines and for animated elements above a stated area fraction |
| C9 | No element at or below body size with a long text run carries a text shadow | H5 | computed style over text nodes |
| C10 | Reading matter has no entry animation | H5 | assert paragraphs, lists and tables carry no animation name |
| C11 | Contrast measured from rendered colours, not from the token file | H6 | script computes foreground against resolved background per text node (EV-0027, EV-0236) |
| C12 | Kicker and caption tiers clear the house target, not only the floor | H6 | same run, compared against the tier table in `packs/pattertech-house/refs/BUDGETS.md` |
| C13 | Every figure node sits on its datapoint within tolerance | H7 | compare rendered node positions against the source data through the kit's scale helpers |
| C14 | No label or box intersects a line, and at most one endpoint accent per figure | H7 | geometry check over the rendered figure |
| C15 | No house number appears outside the budgets file | H8 | source scan for the named values, with an allowlist for the budgets file itself |
| C16 | No horizontal page scroll at any supported width, narrowest included | layout | headless browser, scroll width equals client width at each tested viewport, every changed route |
| C17 | Section text is identical with scripting disabled | H5, degradation ladder | two headless runs, compare text content |
| C18 | Page image transfer inside budget after a full scroll | budgets | headless run totalling image bytes |
| C19 | Every animated custom property is registered in the token layer | defaults | parse registrations, cross-reference against animated property names |
| C20 | Every looping conduit holds offscreen for most of its cycle | H3, budgets | parse the keyframes block, assert the travelling stop sits at or below a tenth of the cycle and the remaining stops hold the offscreen transform; a two-stop `from`/`to` translate fails, and a core on screen for most of the period is a persistent slow traveller and must sit on a monument |

C11 needs a real browser engine, because contrast depends on computed
style and does not resolve in a simulated document (EV-0236). C15 is the
check that keeps H8 honest: without it, a number gets restated in a
component and the two drift, which is the failure that produced this
pack.

## Judgement, recorded not automated

| # | Check | Verifies | What good looks like |
| --- | --- | --- | --- |
| J1 | The container matches what the content is | H1, GD-HOUSE-002 | the reviewer can say in one sentence what the content is, and the container follows from it |
| J2 | A first-time reader can name a moment on the page | GD-HOUSE-001 | someone who has not seen the page names one, unprompted |
| J3 | No single component looks glowing in a screenshot | GD-HOUSE-001 | light is visible in the periphery and deniable up close |
| J4 | The light posture matches the brand's physics | GD-HOUSE-001 | the posture is named in the lock-book with the reason |
| J5 | The register decision is recorded with its cost | GD-HOUSE-003 | the ruling names what the polarity choice costs the smallest type |
| J6 | At most one figure per piece carries a distinguishing device | GD-HOUSE-004 | the promoted figure is named, and the device is outside the plot area |
| J7 | The section would not survive being dropped into a generated site unchanged | anti-patterns | the reviewer names what is specific to this venture |
| J8 | Copy reads as though a person wrote it | voice law | read aloud before shipping |
| J9 | Departures from this pack are written in the lock-book | authority | one line naming the rule and the reason, no waiver machinery |

J7 is the generic-tell test. It is useful and unfalsifiable, it has no
oracle a cold agent can run, and it is deliberately left to a person.
Anything that can be mechanised out of it belongs in the table above
instead.

## What is not checked here

Keyboard operation, pattern conformance, token generation, overlay
absence and field performance are all verified in
`packs/ui-ux/CHECKS.md` and are not duplicated. A house surface passes
those first, then these.
