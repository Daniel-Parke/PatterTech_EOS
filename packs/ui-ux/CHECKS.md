---
summary: What a reviewer or checker can verify about interface work, split into executable today and judgement
kind: fact
scope: estate
sources: [EV-0027, EV-0028, EV-0030, EV-0065, EV-0233, EV-0235, EV-0236, EV-0237]
volatility: slow
review: on-change-of:WCAG-2.2
type: implementation
tags: [a11y, testing, tooling]
---

# CHECKS

Evaluation criteria for work in this domain. Each row says what is
verified, against which requirement, and whether a machine can settle
it today. "Executable" means a script can decide it without a human
reading the output. "Judgement" means a person rules, and the record is
the evidence.

## Executable today

| # | Check | Verifies | How |
| --- | --- | --- | --- |
| C1 | Token source parses and validates against the pinned format version | B6 | schema validation of the source file |
| C2 | Generated token outputs exist for every consuming platform | B6 | file existence per configured platform |
| C3 | Regeneration produces no diff | B6 | run the build, then a clean-tree assertion |
| C4 | One shared implementation per component across surfaces | default in GD-UIUX-002 | grep or import graph, fail on duplicates |
| C5 | Zero scanner violations, tags pinned to the claimed version and levels, real browser | B1, B2 | scanner run per route in CI |
| C6 | Manual verdict file entry count equals the scanner incomplete count | B2 | compare counts, fail on mismatch |
| C7 | Six failure classes asserted individually | B3 | one test each: contrast, image alternatives, form labels, empty links, empty buttons, page language |
| C8 | Keyboard contract per interactive component | B4 | tab order reaches every control, focus visible in computed style, pattern keys produce the stated state change |
| C9 | States manifest exported and each state renders | B7 | manifest walk, one assertion per state |
| C10 | Decisions file names one philosophy per surface with at least one evidence id | B8 | schema validation of the decisions file |
| C11 | Evidence ids in the decisions file exist in the ledger | B8 | lookup against the evidence registry |
| C12 | No overlay script in either build output | B5 | scan built assets for known vendors and for runtime accessibility patchers |
| C13 | No horizontal page scroll at the narrowest supported width | layout reference | headless browser, scroll width equals client width, every changed route |
| C14 | Performance budget respected | performance default | headless run, total bytes after a full scroll, fail over budget |
| C15 | No raw value re-typed where the token scale already names it | B6 | source scan with a written allowlist |
| C16 | Surfaces with different philosophies differ measurably | B8 | computed type scale, spacing density and component inventory differ by a stated threshold |

C5 needs a real browser engine: contrast checks depend on computed
style and do not run in a simulated DOM (EV-0236). C7 is separate from
C5 on purpose, so an aggregate pass cannot hide a regression in the six
commonest defects (EV-0235).

## Judgement, recorded not automated

| # | Check | Verifies | What good looks like |
| --- | --- | --- | --- |
| J1 | Each scanner incomplete has a real verdict | B2 | a sentence naming what was inspected and the conclusion, not "looks fine" |
| J2 | The philosophy fits the surface | B8, GD-UIUX-001 | triggers named, runner-up named, cost of not taking it stated |
| J3 | Pattern deviations are justified | B4 | the deviation, the reason, and the test that pins the shipped behaviour |
| J4 | Alternative text says what the image is for | B3 | a caption-like test: would the sentence still work with the image removed |
| J5 | Error messages say what to do next | B7, forms | plain language, at the summary and at the field |
| J6 | Defaults departed from carry a recorded reason | defaults section | the reason is in the task record, not in a commit message alone |
| J7 | Dashboard answers one named question | dashboard default | the question is written in the surface, panels ordered to answer it |
| J8 | Copy reads as though a person wrote it | voice law | read aloud before shipping |

A heuristic review is cheap and repeatable and gives reviewers a shared
vocabulary for naming defects (EV-0233). Use it to phrase J2 to J7
findings. Do not use it as a conformance claim: the heuristics come
from a 1994 analysis of one problem catalogue, published by a
consultancy that sells training on them, and there is no evidence that
following them improves outcomes.

## Not verifiable here

- Whether a philosophy outperforms its alternatives. No evidence in
  this pack supports that comparison, so no check claims it.
- Whether the surface is accessible. The machine checks find a minority
  of defects (EV-0236, EV-0104 disagree on how small a minority), and
  assistive-technology and user testing sit in GD-UIUX-003 option D.
- Whether a performance improvement caused a business outcome. That
  needs an experiment (EV-0241).

## Cadence

C1 to C12 and C15 run on every change set. C13, C14 and C16 run on any
change touching layout, assets or tokens. The judgement rows run at
review, and J2 runs once per surface at the point the philosophy is
chosen, then again if the surface's audience changes.
