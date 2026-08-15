---
id: GD-API-005
summary: How does a consumer walk a collection: offset paging, opaque cursors, visible keyset, or a hybrid with an estimated total?
kind: wargame
type: wargame
tags: [arch, data, eos, perf, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-API-006]
applies_when: [exposes_service_boundary]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0130, EV-0134, EV-0131, EV-0128]
review: on-change-of:EV-0130
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-API-005: how does a consumer walk a collection?

## Decision question and stakes

Any collection that can grow needs a traversal scheme, and the scheme is
contract: changing it later breaks every client that walks. The fork is
what the client is allowed to know about its position. The failure that
decides it is the drifting window, where rows inserted mid-walk cause a
consumer to skip or duplicate records and nobody notices until the
totals disagree.

## Doctrines or coverage gap under pressure

- `DOC-API-006` (default): Cursor pagination with opaque tokens, no offset.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Does the collection mutate while a client is walking it?
- Does a human need to jump to page 47, or does a machine need every
  row exactly once?
- How large can the collection get?
- Is a total count needed, and does it need to be exact?

Applicability is `exposes_service_boundary`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Offset and limit

Assume `A. Offset and limit` was selected and the outcome failed. Test this option's stated failure mechanism first: rows shifting under the walk cause skips and duplicates; deep offsets get slower and slower because the database still counts past rows; the client learns the collection's internal ordering.

### Premortem for B. Opaque cursor tokens

Assume `B. Opaque cursor tokens` was selected and the outcome failed. Test this option's stated failure mechanism first: , and freedom to change the underlying strategy without breaking clients. Costs: opacity forbids jump-to-page-N and resume-from-arbitrary-position, which some consumers expect.

### Premortem for C. Visible keyset

Assume `C. Visible keyset` was selected and the outcome failed. Test this option's stated failure mechanism first: the sort key becomes public contract and cannot change; it leaks internal ordering and sometimes identifiers; it only works over a key that is unique and monotonic in the sort order.

### Premortem for D. Cursor plus an estimated total

Assume `D. Cursor plus an estimated total` was selected and the outcome failed. Test this option's stated failure mechanism first: someone will treat the estimate as exact and reconcile against it; it must be named so that mistake is hard.

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

## Safe default

B. Opaque tokens, bound to filter and ordering, no `offset` parameter
declared on the operation, next token in the response body.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Does the collection mutate while a client is walking it?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B. Opaque tokens, bound to filter and ordering, no `offset` parameter declared on the operation, next token in the response body.

**Exit condition:** Stop or roll back the selected branch when rows shifting under the walk cause skips and duplicates; deep offsets get slower and slower because the database still counts past rows; the client learns the collection's internal ordering, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Does the collection mutate while a client is walking it?

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 1 worked ruling note. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
