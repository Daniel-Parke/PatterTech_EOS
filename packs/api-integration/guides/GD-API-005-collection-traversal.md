---
summary: How does a consumer walk a collection: offset paging, opaque cursors, visible keyset, or a hybrid with an estimated total?
kind: guide
authority: advisory
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0130, EV-0134, EV-0131, EV-0128]
review: on-change-of:EV-0130
type: guide
tags: [arch, perf, data]
review_by: 2027-09
---

# GD-API-005: how does a consumer walk a collection?

## The question

Any collection that can grow needs a traversal scheme, and the scheme is
contract: changing it later breaks every client that walks. The fork is
what the client is allowed to know about its position. The failure that
decides it is the drifting window, where rows inserted mid-walk cause a
consumer to skip or duplicate records and nobody notices until the
totals disagree.

## It depends on

- Does the collection mutate while a client is walking it?
- Does a human need to jump to page 47, or does a machine need every
  row exactly once?
- How large can the collection get?
- Is a total count needed, and does it need to be exact?

## Options

### A. Offset and limit

`?offset=200&limit=50`. Buys: trivial to implement, jump-to-page works,
every ORM does it natively, and it stays conformant under specifications
that deliberately take no position (EV-0134). Costs: rows shifting under
the walk cause skips and duplicates; deep offsets get slower and slower
because the database still counts past rows; the client learns the
collection's internal ordering.

### B. Opaque cursor tokens

A `page_token` or `cursor` the server issues and the client returns
verbatim, with a next-token field in the response. Tokens are
non-parseable, bind to the filter and ordering of the issuing call so a
mismatched follow-up is an error, and never carry authorisation; total
counts are optional and may be estimates (EV-0130). Buys: stable walks
over mutating data, no deep-offset cost, and freedom to change the
underlying strategy without breaking clients. Costs: opacity forbids
jump-to-page-N and resume-from-arbitrary-position, which some consumers
expect.

### C. Visible keyset

`?after_id=...&limit=50` over a sortable key. Buys: cursor-like
stability with a value the client can reason about and reconstruct after
losing state. Costs: the sort key becomes public contract and cannot
change; it leaks internal ordering and sometimes identifiers; it only
works over a key that is unique and monotonic in the sort order.

### D. Cursor plus an estimated total

B with a `total_estimate` field, explicitly documented as approximate.
Buys: the progress bar a UI wants without the exact-count query cost.
Costs: someone will treat the estimate as exact and reconcile against
it; it must be named so that mistake is hard.

## Decision rule

- Machine consumers, exports, sync jobs, anything that must see each row
  once: B.
- Collections that mutate while being walked: B or C, never A.
- A human table UI that genuinely needs page numbers: A or C, with the
  reason recorded next to the code and a bound on the maximum offset.
  This is a real deviation from the default, not a lapse.
- Progress indication needed over a large collection: D.

Whatever the choice, no endpoint mixes offset and cursor parameters, and
the response advertises its own limits alongside the rate-limit policy
so a client can plan a walk rather than discover the ceiling by being
refused (EV-0128). Zalando reaches the same cursor preference from a
different direction (EV-0131).

## Default

B. Opaque tokens, bound to filter and ordering, no `offset` parameter
declared on the operation, next token in the response body.

## Worked rulings

- **No venture has argued this fork.** The default is inherited from
  the sources, and the first venture with a table UI over a large
  mutating collection should argue A or C properly rather than quietly
  adding an offset parameter.
