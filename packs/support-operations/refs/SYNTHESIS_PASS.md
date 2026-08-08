---
summary: The weekly pass that turns an inbox into backlog items, the declared coding stance, the denominator and the theme record
kind: fact
scope: estate
sources: [EV-0041, EV-0210]
volatility: slow
review: 2028-09
type: implementation
tags: [ops, product, data]
---

# The synthesis pass

Reference for PACK.md D7 and B6. Recording complaints without a
periodic synthesis is a failure of the complaints process rather than a
missed nicety, so this pass is the part of support that pays the
product back.

## Declared before coding, not after

Four choices are written down before any item is read
(EV-0431):

1. **What the data set is.** Which channels, which date range, which
   items were excluded and why.
2. **Inductive or framed.** Whether themes come from the items or from
   an existing frame such as the product's own feature map.
3. **Surface or underlying.** Whether coding reads what was said or
   what it implies about the person's goal.
4. **What counts as a theme.** A stated threshold, so that "a theme"
   is not decided by whichever grouping looks tidiest at the end.

Themes are constructed by the analyst. "A theme emerged" is not an
available sentence, because it hides the decisions that produced it.

## The denominator

Every count is reported against a stated denominator. Eleven tickets
mentioned a thing, out of forty items from thirty-one customers over
one week. Without the denominator the count is not a finding.

Support data is self-selected: only people who contacted you are in it.
Prevalence within the inbox is not prevalence within the user base, and
saying so once per report is cheaper than the argument that follows
when someone assumes otherwise.

## The theme record

| Field | Meaning |
| --- | --- |
| `denominator` | the population every count is drawn from, stated in full |
| `coding_stance` | the four declarations above, in one place |
| `themes[]` | one entry per theme |
| `themes[].name` | what the theme is |
| `themes[].count` | how many items, equal to the length of the item list |
| `themes[].item_ids` | the item ids, all of which exist in the triage record |
| `themes[].proposed_action` | the backlog item, or nothing |

Item ids are ids. Customer names, addresses and account numbers do not
appear in a synthesis file (PACK.md B6, EV-0041).

An item may sit in more than one theme. The distinct ids across all
themes cannot exceed the size of the data set, which is the one
arithmetic check worth running automatically.

## What the pass does not do

It does not rank by revenue or by segment. The method offers no way to
tell a rigorous theme from a small vocal minority, so weighting is a
separate product decision taken with the counts in hand rather than
smuggled into the coding.

It does not produce a single health number. No one number captures a
system, which the estate already accepts elsewhere (EV-0210).

## Cadence

Weekly while one person handles the queue, because the pass is also how
that person notices they have stopped learning. Monthly once support
has its own owner, with the weekly counts kept so the trend survives.
