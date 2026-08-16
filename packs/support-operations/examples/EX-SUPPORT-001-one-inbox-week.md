---
summary: The pack applied end to end over one week of forty inbound items for a paid product with sixty customers, including one customer-visible outage
kind: example
scope: estate
type: example
tags: [ops, product, pii, money]
---

# EX-SUPPORT-001: one inbox week and one outage

The situation. A two-person venture sells a scheduling tool to sixty
paying customers. One founder answers everything. Over one week, forty
items arrive: twenty-four questions, eight bug reports, five feature
requests, two billing complaints, and one outage report that four later
items repeat independently without knowing about each other. Three
reports contain no reproduction detail at all. This is the pack applied
in order, with the decisions written as they were taken.

## 1. Pick the patterns before opening the inbox

Under `packs/support-operations/wargames/WG-SUPPORT-001-triage-pattern.md`
the venture has paying customers and one responder, so it runs D plus A
plus C: founder-delivered support as the posture, severity-first
handling for anything availability-shaped, and the complaints loop for
anything a paying customer frames as a complaint. It does not run a
public tracker, so no auto-close timer exists anywhere.

The exit signal from D is written the same day: move off founder
support at whichever comes first of responder utilisation above seventy
per cent for two consecutive weeks, or a month in which no contact
teaches anything new (PACK.md D8, D11).

## 2. Write the ladder before touching item 1

Three bands, most urgent first, each with an impact criterion, the
tie-break stated in the file, and S1 named as the band that changes the
response mode. The three-factor declaration score and the combining
rule are written alongside it. Shape and wording follow
`packs/support-operations/references/SEVERITY_AND_DECLARATION.md`.

Nothing in it is invented during the incident, which is the entire
reason it exists (PACK.md B2).

## 3. Triage all forty, then rank

Classification comes first, prioritisation second (PACK.md B1). Each of
the forty gets one record with `kind`, `priority`, `queue` and
`triage_state`. The queue vocabulary is `incident` and `request`, and
no item sits in both (PACK.md D1).

- The outage report and its four independent duplicates all carry the
  same `incident_id`. One cause, one record, one answer, and the
  duplicate count of four is itself reported as a count.
- The three reports with no reproduction detail go to `needs-info` with
  `next_action_due` four days out, under option C of
  `packs/support-operations/wargames/WG-SUPPORT-002-close-policy.md`. They
  are not closed, because the venture never asked the question that
  would have produced the missing detail.
- The two billing complaints get `acknowledged_at` the hour they
  arrive, and carry no timer field of any kind, so that no later
  tooling change can quietly apply one (PACK.md D3).
- Five feature requests land in the reserved plausible-but-unevidenced
  band rather than being argued into or out of the roadmap on the spot
  (PACK.md D5).

Untriaged count at the end of the pass: zero. That number only exists
because `triage_state` is a field.

## 4. Declare, run and tell

Scored under
`packs/support-operations/wargames/WG-SUPPORT-003-declaration-route.md`:
core path, customers affected now, twenty minutes elapsed, low
confidence of a fix within the hour. It declares at S1.

`declared_at`, `declared_by`, `comms_owner`, `fix_owner`,
`customers_affected` are all recorded. The founder is both owners, and
both fields are filled with the same name, because the record has to
show the decision was taken rather than skipped (PACK.md B3).

The communication log carries four entries with increasing timestamps,
the first well before resolution, each naming its audience: affected
customers at declaration, all customers twenty minutes later, affected
customers again when the workaround is confirmed, and everyone at
resolution.

**The honest all-clear.** The fix went out with the integration suite
skipped, because the suite takes eighteen minutes and the outage was
live. The resolution message says exactly that: service restored, fix
deployed with the integration suite skipped, full verification run
scheduled within two hours, next update either way. Nothing claims a
check passed that did not run (PACK.md B4,
`packs/support-operations/references/INCIDENT_COMMS.md`).

`postmortem_due` is set at resolution, three days out, with a named
owner (PACK.md D9).

## 5. Turn the week into backlog

The synthesis pass follows
`packs/support-operations/references/SYNTHESIS_PASS.md`. Written before any
item is reread: the data set is all forty items from this week's
inbox, coding is framed by the product's feature map, it reads the
surface, and a theme needs three or more items.

Denominator recorded in full: forty items from thirty-one distinct
customers, of sixty, over seven days. Four themes result, each with a
count equal to the length of its item id list, every id present in the
triage record. Two convert to backlog items, one converts to a
documentation fix, one is recorded and left alone.

The report notes in one line that prevalence in the inbox is not
prevalence in the user base, because twenty-nine customers said nothing
at all this week.

## 6. The numbers reported, and the ones not

Reported: counts by kind, duplicate count against the one incident,
untriaged count of zero, reopened count, and the outage duration as a
single raw figure. No average of any duration appears, and no band
carries a time target (PACK.md B5).

Not collected: a loyalty score, because at sixty customers nobody could
name a decision it would change, and no source in the pack says what
sample size makes it stable. Not collected: a deflection rate, because
the pack found no primary evidence that it tracks any customer outcome.
Both omissions are written down, so the next person argues with a
decision rather than assuming an oversight.

## 7. What left the building

The triage file, the theme report and the public incident note carry
item ids and account ids. No customer name, email address or account
number appears in any of them (PACK.md B6). Nothing was pasted into an
outside summarising tool, because no lawful basis for that transfer had
been recorded.

## What this example is not

It is one week, one venture, one responder, and no rota. The utilisation
arithmetic that sets the exit signal assumes a single server with no
priority classes and nobody giving up, so a busier desk with real
prioritisation behaves differently in detail while collapsing the same
way.
