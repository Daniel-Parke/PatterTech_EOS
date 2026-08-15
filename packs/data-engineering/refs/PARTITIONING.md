---
summary: Choosing the partition column and width, deriving the value safely, evolving the layout, and the two failure directions
type: implementation
tags: [data, ops, state]
kind: recipe
scope: estate
review: 2028-06
sources: [pending-import]
---

# Partitioning

Level-3 reference for default D4 in `packs/data-engineering/PACK.md`.
The partition is the unit of replacement, which makes it the unit of
reprocessing, which makes this decision upstream of most of the pack.

## Choose the column first

Partition on the thing a correction is scoped by. For a pipeline that
reprocesses a day at a time, that is the event date. Partitioning on
anything else means a correction cannot be expressed as a replacement,
which pushes the table onto the merge path in
`packs/data-engineering/guides/GD-DATAENG-002-idempotent-reprocess.md`
and its dependency on a reliable key.

A second partition column is a decision to justify, not a free
refinement. It multiplies the file count by its cardinality.

## Then the width

| Rows per day | Sensible width |
| --- | --- |
| Under a hundred thousand | None. Do not partition. |
| Hundreds of thousands | Month, or day if reprocessing is daily |
| Millions | Day |
| Tens of millions and a latency need | Hour |

The two failure directions are not symmetric. Too coarse costs read
time and forces a bigger unit of reprocessing, and both are visible and
fixable. Too fine produces a small-file problem, which degrades slowly,
shows up as unexplained slowness, and is dull to unpick. When in doubt,
coarser.

## Derive the value in one place

The partitioning documentation for the table format is the sharpest
source in this pack on why. When the writer supplies the partition
value, nothing can check it: the wrong format, the wrong time zone, or
the wrong source column, and it names using the processing time in place
of the event time as exactly that mistake, all land a wrong answer while
every query keeps succeeding. Readers inherit the same trap, because a
query filtering only the real column scans everything.

Two ways out, in order of preference:

1. **Declare the partition as a transform of a real column** and let the
   engine derive and apply it. The value is then correct by
   construction, the reader does not need to know the layout, and the
   layout can change later.
2. **One function owns the derivation.** Where the format cannot hide
   the partition, no call site formats a date. One function takes the
   event timestamp and returns the partition value, everything calls it,
   and the test for it is worth more than the test for the transform.

Writing the partition value at the call site is the pattern D4 exists to
refuse.

## Evolving the layout

Changing the partition scheme on a format that supports it is a metadata
change: existing files keep the scheme they were written with, new files
take the new one, and a reader plans both separately. Nothing is
rewritten.

Two consequences, both underplayed by the source that describes it:

- It is cheap to declare and not free to read. A long-lived table can
  end up carrying several layouts, each planned separately.
- The old data is still laid out the old way, so a reprocess of an old
  window replaces files under the old scheme unless the run rewrites
  them deliberately.

Treat an evolution as a decision with a follow-up, not as a fix.

## Where the format cannot help

A venture writing partitioned files into object storage with no table
format has none of this. The transferable parts are the ones that
survive: partition on the correction axis, derive the value in one
function, keep the width coarse, and record the layout somewhere a
reader will find it. The part that does not survive is safety: nothing
will catch a wrong value, so the function that derives it carries the
whole burden and should be tested as though it did.

## Not covered here

Sort order, clustering, file sizing and compaction cadence are
preferences in `packs/data-engineering/PACK.md` until read time
complains. Whether the table is wide or star-shaped, and what its grain
is, belongs to `packs/data-analytics/PACK.md`.
