---
summary: Single-run cold-agent acceptance drill for positioning, testing whether the marketing pack produces a defended position or a feature list with adjectives
type: example
tags: [eos]
---

# DRILL-MKTG-002: a position that excludes somebody

## Scenario

A cold agent is given the `marketing-growth` pack and a repository
holding a real product: a scheduling tool for independent physiotherapy
practices, with a README, a pricing page and eleven support tickets in
`support/tickets/`. There is no positioning document.

The prompt is one line: "Write the positioning for this product."

Single run, no follow-up prompts.

The existing marketing drill covers campaign mechanics and measurement.
Neither it nor any other drill touches positioning, which is the part
of the pack an agent is most likely to answer with adjectives.

## Deterministic criteria

1. A positioning document exists at a single recorded path.
2. It names the competitive alternative the buyer would use instead,
   including the do-nothing or spreadsheet alternative where that is
   the real one, and does so as a named thing rather than a category.
3. It names at least one segment the product is explicitly **not** for,
   in a sentence a reader could act on. "Not for everyone" fails.
4. Every capability claimed is tied to an attribute of the product that
   a reader can check in the repository, by path or by feature name.
5. Each claimed value maps to at least one of the eleven tickets by id,
   or is marked as unevidenced with that word.
6. No claim uses a superlative or a category-leadership phrase
   ("best in class", "leading", "world-class", "revolutionary").
7. The document states who the buyer is and who the user is, and says
   whether they are the same person for this product.
8. A pricing statement exists that is consistent with the pricing page
   in the repository; a contradiction between the two fails.
9. The document records at least one alternative position that was
   considered and rejected, with the reason.
10. The document carries a review trigger naming the event that would
    invalidate it, not a date alone.

## What a position has to do

Criterion 3 is the one this drill exists for. A position that excludes
nobody has not been taken, and it is the criterion an agent trained to
be helpful is most likely to soften. A document that lists every
plausible buyer and then ranks them does not satisfy it: the pack asks
for a segment the product is not for, and the test is whether a reader
could use the sentence to disqualify a lead.

Criterion 5 is the second. The tickets are in the repository so that a
claim about what customers want has somewhere to come from other than
the model's prior.

## Fail conditions worth logging separately

- Every criterion passes except 3: the pack taught the template and not
  the trade-off.
- Claims present, ticket ids absent (5 fails while 4 passes): the
  product was read and the customers were not.
- The agent produces a launch plan or a channel mix instead: the pack
  did not carry positioning as work distinct from campaigns.

## Freeze note

Criteria 1 to 10 are frozen. The product repository, its pricing page
and the eleven tickets are fixed inputs and are stored with the drill.
This drill was written after the `marketing-growth` pack was authored,
so it is not an independent oracle; `frozen_before_authoring` is false
in the manifest.
