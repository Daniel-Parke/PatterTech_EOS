---
summary: What a reviewer or a script can verify about support work, split into executable today and judgement
kind: record
scope: estate
sources: [EV-0041, EV-0200, EV-0210, EV-0211]
volatility: slow
review: on-change-of:ISO-10002-revision
type: checks
tags: [ops, product, testing, tooling]
---

# CHECKS

Evaluation criteria for support work. Each row says what is verified,
against which requirement, and whether a machine can settle it today.
"Executable" means a script can decide it without a person reading the
output. "Judgement" means a person rules and the record is the
evidence. A check that needs a person is still a check.

B4 and B6 bind. B1, B2, B3, B5 and B7 are defaults since the ADR-0008
audit, so the rows behind them still run and a venture that departs
records why. A row that fails against a default is a finding to be
answered in writing, not a finding to be waved through.

## Executable today

| # | Check | Verifies | How |
| --- | --- | --- | --- |
| C1 | One triage record per inbound item, no duplicates, no extras | B1 | count records against the inbound set, compare id sets |
| C2 | Every record has non-empty kind, priority, queue and triage_state | B1 | field presence scan, fail on any empty |
| C3 | triage_state is one of accepted or needs-info | B1 | enum check |
| C4 | Queue values partition, with no item in two queues | B1, D1 | set intersection across queues must be empty |
| C5 | Every needs-info record carries next_action_due strictly after its triage date | B1, D3 | date comparison per record |
| C6 | No record from a paying customer carries an auto-close or timer field | D3, D4 | key scan against the channel's customer list |
| C7 | Every complaint record has acknowledged_at set | D3 | field presence on kind equals complaint |
| C8 | Duplicate reports of one cause share one incident or defect id | B1 | group by cause id, assert one work record per group |
| C9 | The severity ladder file exists, has three or more ordered bands each with a written impact criterion, states the take-the-higher rule, and names one band that changes response mode | B2 | parse the ladder file, assert all four properties |
| C10 | The incident record carries severity, declared_at, declared_by, comms_owner, fix_owner, customers_affected, resolved_at, postmortem_due | B3, D9 | key presence check |
| C11 | severity is a band defined in the ladder file | B2 | membership test against the parsed ladder |
| C12 | comms_owner and fix_owner are separate non-empty fields, even where the values are equal | B3 | two-key presence check, equality allowed |
| C13 | postmortem_due is at most five days after resolved_at | D9 | date arithmetic |
| C14 | The communication log has three or more entries with strictly increasing timestamps, the first before resolved_at, each naming an audience | B4, comms reference | parse log, assert ordering and audience field |
| C15 | No published file carries a key, heading or target naming an average or a mean of a duration | B5 | key and heading scan, fail on any average-of-duration name |
| C16 | Any duration reported carries a percentile label or is a raw count | B5 | scan duration fields for a percentile or count marker |
| C17 | The synthesis file has denominator, coding_stance and a themes array | D7 | schema validation |
| C18 | Every theme count equals the length of its item id list, and every id exists in the triage record | D7 | arithmetic and lookup |
| C19 | Distinct item ids across all themes do not exceed the size of the declared data set | D7 | set size comparison |
| C20 | No customer name, email address, phone number or account number appears in any derived or published file | B6 | match derived files against the customer list, allow hashed or id forms only |
| C21 | Any loyalty or satisfaction figure is shown with its population, its n and its date range | B7 | field presence beside the figure |
| C22 | Responder utilisation is computed and recorded for the period | D8 | presence and range check on the utilisation figure |

C15 and C16 are separate on purpose: banning the name is not the same
as proving what remains is a percentile or a count. C20 needs the
customer list at check time and must never write it into its own
output.

## Judgement, recorded not automated

| # | Check | What good looks like |
| --- | --- | --- |
| J1 | The severity band fits the impact criterion it claims | someone who was not in the incident can read the criterion and reach the same band |
| J2 | No message reported a bypassed check as passing | every skipped, waived or emergency-route gate appears in the record and in the message, in those words (B4) |
| J3 | The all-clear names what was verified and by what | "resolved" alone is a finding, not a message |
| J4 | Stated causes are supported by the record | "cause unknown" present where the record does not settle it |
| J5 | The coding stance was written before coding, not after | the four declarations are dated ahead of the first coded item (D7) |
| J6 | Themes are argued rather than announced | no sentence claims a theme emerged; the grouping rule is stated |
| J7 | Prevalence claims are scoped to the inbox | the report says once that inbox prevalence is not user-base prevalence |
| J8 | The answer to a duplicated defect is the same answer | the shared record's reply text is what every reporter received |
| J9 | Needs-info was not used to park work | on the due date, someone chased, closed with an answer, or converted |
| J10 | The founder-support exit signal is written and still true | recorded on the day the posture started, and re-read this quarter (D11) |
| J11 | A metric that nobody acts on is retired | for each reported number, name the decision it changed in the last quarter |
| J12 | Departures from defaults carry a recorded reason | the reason is in the task record, not in a commit message alone |

## Not verifiable here

- Whether self-service deflection helps any customer. No primary source
  in this pack supports the claim, so no check asserts it.
- Whether a support pattern improves retention. None of the sources
  measures that; the complaints standard and the service management
  standard are consensus practice, not findings.
- Whether a loyalty score is stable at this venture's sample size.
  Neither the original claim nor its replication addresses small n.
- Whether support volume leads churn. Plausible, widely asserted, no
  primary source located.
- Whether the response was fast enough. No source here supports a
  response-time target, and no check invents one.

## Cadence

C1 to C8 run on every triage pass. C9 to C16 run at incident
resolution and again at postmortem. C17 to C19 run on every synthesis
pass. C20 runs on every file that leaves the system of record. C21 and
C22 run whenever a number is reported. The judgement rows run at the
postmortem and at the weekly synthesis, and J10 runs quarterly.
