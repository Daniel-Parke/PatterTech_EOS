---
summary: Cold-agent acceptance drill for the ui-ux pack, two philosophies, one behaviour core, machine-checked
type: example
tags: [eos]
---

# Drill: two surfaces, one spine

Single run, cold agent, no human turns, pack plus this brief only.

## Brief handed to the agent

Build, in one repo, two surfaces sharing one token source and one
headless behaviour layer: `surfaces/service/`, a content-first
public-service task flow with a three-field form, error summary and
check-answers page; and `surfaces/dashboard/`, a data-heavy operations
dashboard answering one named question with four panels and written
panel context. Record the philosophy choice per surface in
`DESIGN_DECISIONS.md`.

## Deterministic acceptance criteria

Pass requires every check below. Each is a script exit code.

1. `tokens/tokens.json` parses and validates against the DTCG format;
   generated outputs exist for at least two platforms and are byte
   identical to a fresh regeneration from source.
2. No generated token file is edited by hand: regeneration produces no
   diff (`git diff --exit-code` after the build).
3. Both surfaces import interactive components from one shared module
   path; a grep asserts zero duplicate component implementations across
   the two surfaces.
4. axe run in a real browser over every route returns zero violations
   at pinned WCAG 2.2 A and AA rule tags; every `incomplete` result is
   listed in `A11Y_MANUAL.md` with a written verdict, and that file's
   count equals the axe report's.
5. The six WebAIM failure classes are individually asserted by explicit
   tests: contrast, image alt text, form labels, empty links, empty
   buttons, declared page language.
6. Keyboard contract test per interactive component: tab order reaches
   every control, visible focus is present in the computed styles, and
   the APG-specified keys for that pattern produce the specified state
   change.
7. Every component exports a states manifest naming focus, hover,
   active, disabled, loading and error; a test asserts each named state
   renders.
8. `DESIGN_DECISIONS.md` names one philosophy per surface from the
   pack's list and cites at least one evidence id per choice; a schema
   check validates the file.
9. The two surfaces differ measurably: computed type scale, spacing
   density and component inventory differ by a stated threshold, so a
   single house style cannot satisfy both.
10. No accessibility overlay script, third-party or hand-rolled, appears
    in either build output.

## Failure signals to record

Same visual style applied to both surfaces; tokens edited by hand after
generation; a11y checks green while `A11Y_MANUAL.md` is empty; keyboard
tests asserting render only, never key behaviour.
