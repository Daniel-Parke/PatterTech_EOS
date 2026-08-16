---
summary: The field shape of a triage record, the four independent axes, the queue vocabulary, deduplication and the needs-info clock
kind: fact
scope: estate
sources: [EV-0041]
volatility: slow
review: on-change-of:ISO-10002-revision
type: implementation
tags: [ops, product, pii]
---

# Triage record

Reference for PACK.md B1 and B6, and for
`packs/support-operations/wargames/WG-SUPPORT-002-close-policy.md`. This
is the field shape. The policy behind each field is in PACK.md.

## One record per inbound item

One record per item, keyed by the item's own id, with no duplicates and
no records for items that did not arrive. The record is the queryable
object: if a state cannot be expressed as a field value, it is not a
state, it is an absence.

## The four axes, independent

| Field | Meaning | Notes |
| --- | --- | --- |
| `kind` | what sort of thing it is | question, bug, feature-request, complaint, billing, other |
| `priority` | how soon it matters | one band is reserved for plausible but unevidenced, PACK.md D5 |
| `queue` | who or what handles it | closed vocabulary, see below |
| `triage_state` | `accepted` or `needs-info` | untriaged is expressed as the record not yet existing, never as an empty field |

The axes stay separable. Collapsing kind, urgency and owner into one
P-number is the anti-pattern named in PACK.md, and it is detectable:
after the collapse, no query answers anything.

## Queue vocabulary

At minimum `incident` and `request`, per PACK.md D1. An item sits in
exactly one queue, and the two carry different targets, because
restoring an interrupted service and fulfilling a routine ask are
different jobs. A venture may add queues; it may not put one item in
two.

## Deduplication

Where one cause explains several reports, every report carries the same
`incident_id` or `defect_id`, and that id is the id of the record where
the work happens. One cause, one record, one answer. The count of
duplicate reports against a cause is a useful number in its own right
and is reported as a count, never as a rate without a denominator.

## The needs-info clock

A `needs-info` record carries `next_action_due`, a date strictly after
the day it was triaged. On that date a person chases, closes with an
answer, or converts the item to a defect on the evidence already held.
The clock exists to make the state reviewable. It is not an auto-close
timer, and no auto-close timer field is present on any record from a
paying customer.

## Complaint fields

A complaint carries `acknowledged_at`, set when receipt was
acknowledged, and closes only when the complainant has been told the
outcome. That is PACK.md D3, and it is why a timer field on a
complaint record is a defect in the record rather than a
configuration choice.

## Personal data

Ticket bodies hold personal data. Derived files such as triage exports,
theme reports and anything published carry ids or salted hashes, never
names, email addresses, phone numbers or account numbers (PACK.md B6,
EV-0041). Retention is set once per channel. An export to any tool
outside the system of record needs the recorded lawful basis first.
