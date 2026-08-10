---
summary: Single-run cold-agent acceptance drill for a greenfield non-PatterTech interface, testing that the pluralism contract survives contact with a brief the house style does not fit
type: example
tags: [eos]
---

# DRILL-UIUX-002: a greenfield surface that is not ours

## Scenario

A cold agent is given the `ui-ux` pack and an empty repository, and is
told it is building the first screens for **Almsford Clinical**, an
outside client running a dosage-calculation tool for hospital
pharmacists. The brief states: clinical, high-density, print-adjacent,
read under fluorescent light on a ten-year-old display, and the client
has an existing brand of navy and white with a grotesque typeface.
Nothing in the brief mentions PatterTech.

The prompt is one line: "Set up the interface foundations and build the
dosage entry screen."

Single run, no follow-up prompts.

This drill exists because the estate's own house pack is adoption-gated
and the `ui-ux` pack says plainly that it does not rank the eight
philosophies. Both claims are cheap to make and only testable on a
brief the house style is wrong for. `pattertech-house` is not activated
here and must not be consulted.

## Deterministic criteria

1. A philosophy record exists, names exactly one philosophy from the
   list in `packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md`, and
   cites at least one evidence id that resolves in the ledger.
2. The recorded philosophy is one whose stated triggers match the
   brief. A record naming a philosophy whose triggers contradict
   clinical density fails, and the record names the runner-up.
3. No file in the delivered tree references `packs/pattertech-house/`,
   and no house token name appears in the source.
4. The delivered palette derives from the client's stated navy and
   white. No warm accent, no terracotta, no amber, no cream ground.
5. The type stack names the client's grotesque or a stated substitute
   with a reason. No serif display face appears.
6. A states manifest exists covering focus, hover, active, disabled,
   loading and error for every interactive component, with any state a
   component cannot enter declared absent and given a reason.
7. Contrast is measured from rendered colours and every text tier
   clears the AA floor, checked in a real browser engine.
8. The six cheap failure classes each carry their own assertion:
   contrast, image alternative text, form labels, empty links, empty
   buttons, declared page language.
9. The dosage entry field has an explicit label, an error message that
   states what to do next, and a value that survives a failed submit.
10. No animation is applied to reading matter or to any numeric field.

## What must not be rewarded

Nothing in this drill scores resemblance to the PatterTech house style,
and a grader that does is broken. A surface that arrives cream, serif
and amber has failed criteria 3 to 5 no matter how well made it is,
because the brief asked for a clinical tool for an outside client.

The inverse is also barred. A grader must not reward a surface for
looking unlike the house style as such: criteria 4 and 5 are keyed to
the client's stated brand, not to distance from ours. A navy clinical
screen and a cream editorial screen are both correct, on the brief that
asked for them.

## Fail conditions worth logging separately

- House aesthetics arrive with no adoption record (3 to 5 fail): the
  pluralism contract is prose and the default is the house style.
- A philosophy is recorded but the surface does not follow it (1 and 2
  pass, 4 and 5 fail): the record is paperwork.
- The agent asks which philosophy to use rather than choosing and
  recording one: the guide did not carry a decision.

## Freeze note

Criteria 1 to 10 are frozen. The brief, the client palette and the
typeface constraint are fixed inputs and are stored with the drill.
This drill was written after the `ui-ux` pack was authored, so it is
not an independent oracle; `frozen_before_authoring` is false in the
manifest and the guarantee is weaker than the Wave A drills carry.
