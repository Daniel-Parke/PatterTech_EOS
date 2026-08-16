---
summary: Pinning model identifiers, recording retirement dates, the migration drill and the scheduled drift check
type: foundation
tags: [ops, delivery, perf]
kind: fact
scope: estate
sources: [EV-0255, EV-0259, EV-0260, EV-0268]
volatility: fast
review: on-change-of:EV-0260
---

# Model migration reference

Level three detail behind binding requirement B4 and Wargame
`packs/ai-ml-llm/wargames/WG-AIML-006-model-lifecycle-and-cost.md`.

## Pinning

Every model identifier in the source is pinned to a version the
provider has undertaken not to move. A moving alias is banned, because
it makes a behaviour change indistinguishable from a deployment and
destroys the ability to attribute a regression to anything.

Pinned does not mean dated. Providers express pinning differently:
some publish a dated snapshot, some publish a version-numbered id with
no date, and at least one major vendor's current ids carry no date and
document that a date suffix must not be appended. Some publish both,
an undated alias beside a dated full id, and only the second is
pinned. Read the provider's own id list and find out which of its
forms is stable, rather than assuming the shape tells you.

The check is therefore a match against the provider's pinned-id
pattern, configured per provider, and a failing match on anything
outside it. A generic date regex is the wrong check and will reject
correct identifiers.

Beside each pin sits the published retirement date. That date is
tentative when it is far out and firm once deprecation is announced,
and it belongs next to the call site rather than in a spreadsheet
somebody remembers in the last week (EV-0260).

## The lifecycle you are buying into

One frontier provider publishes four states, active, legacy,
deprecated and retired, commits to at least sixty days of notice
before retiring a publicly released model, publishes tentative
retirement dates roughly a year or more out, and provides a usage
export so a customer can audit which keys still call a deprecated
model. Requests to a retired model fail outright. API parameters are
deprecated on the same footing, with temperature, top_p and top_k now
returning a 400 on the newest model line (EV-0260).

Sixty days is a floor rather than a comfortable window, one vendor's
policy is not a standard, and partner-operated platforms run their own
schedules. A deployment across two clouds carries two clocks.

## The migration drill

1. **Audit.** Pull the usage export and list every key still calling
   the outgoing model. The list is longer than the codebase suggests,
   because scripts and notebooks call models too.
2. **Freeze the eval.** The acceptance set, the templates and their
   hashes do not change during a migration. Changing the eval and the
   model together makes the result uninterpretable.
3. **Run both.** Old pin and candidate pin, over the same items, and
   report the paired difference with its interval
   (EV-0255). Templates may need adjusting for the new
   model, and if they do, that is a second experiment reported
   separately.
4. **Read the abstention and groundedness rates**, not only accuracy.
   A model that scores the same while abstaining half as often has
   changed behaviour in a way the headline hides.
5. **Re-measure the usable context length** and the cache hit rate.
   Both belong to the model.
6. **Switch behind a flag**, with the old pin still callable until the
   retirement date passes.
7. **Record the provenance row**: provider, pinned id, retirement date,
   documented capability limits and the provider's published model
   documentation (EV-0268).

## The drift check

A pinned name is not a frozen behaviour. The same endpoint changed
substantially across two snapshots, with one task falling from 84 per
cent to 51 per cent, and instruction-following degrading noticeably
(EV-0259). Run the acceptance set on a schedule against the
pinned model, not only when you change something, and treat an
unexplained move as an incident rather than as noise.

## Evidence boundary

The drift study is two snapshots of one vendor's models in 2023, and
the arithmetic result in particular was criticised on the grounds that
the answers changed format rather than capability, so part of the drop
is a parsing artefact. It shows that drift can happen, not how often
it happens now. Providers have since published clearer pinning and
deprecation policies, which bounds the availability risk without
touching the behavioural risk. The lifecycle detail above is a
snapshot of a live vendor page as read on 2026-08-03.
