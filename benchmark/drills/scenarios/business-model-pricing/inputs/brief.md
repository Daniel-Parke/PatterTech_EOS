# Bramble: where we are before we switch charging on

Written for whoever picks up the pricing work. Everything here is what
we know, not what we have decided.

## What we sell

Bramble is a web app for people with an allotment or a kitchen garden in
the UK. Bed planner, sowing calendar, frost and watering reminders, a
photo diary per plot. It runs in a browser and there is no hardware and
nothing to post, except the seasonal planner mentioned below.

Buyers are individuals gardening for themselves. Nobody is buying this
through a company and nobody has asked for an invoice addressed to one.
We have had two enquiries from allotment societies wanting a shared
account; both are parked.

It is a monthly subscription that renews on its own until someone stops
it. We are not planning an annual plan in the first release.

## Where the numbers came from

Two exports live beside this note.

`costs.csv` is twelve months to June 2026 out of the accounting
spreadsheet, one row a month: accounts live in the month, hosting,
support time costed at the rate we pay the part-time helper, third party
tooling (email sending, image storage, error tracking), and the
allocation per active account that falls out of dividing the three by
the account count. The allocation method has not changed over the twelve
months.

`cohorts.csv` is the analytics job, run on 2026-07-02. Eighteen monthly
signup cohorts from January 2025 to June 2026, one row per cohort per
month of age, holding how many of that cohort were still active. Active
means opened the app at least once in the month. Nobody has ever paid,
so there is no revenue column and nothing here is a paying cohort.

Two things to know about the cohort file. Cohorts get shorter as they
get younger, so the January 2025 cohort has eighteen rows and the June
2026 cohort has one. And a lapsed account never comes back in the file:
if someone returns they appear as a new signup, which we know is a
simplification.

## What a buyer would actually pay

The beta banner quotes 5.99 a month. That number came off the back of an
envelope in about four minutes and nobody should treat it as decided.

On top of it, as things stand:

- Our payment provider takes 49p on every monthly payment. We pass it
  straight through and the buyer sees it added at the checkout step.
  There is no way for a buyer to pay us and not incur it, whichever card
  they use.
- There is a one-off 3.00 joining fee on the first payment. Everyone
  pays it. It was meant to cover the setup call we no longer do.
- Extra photo storage above the fair-use line is 2.00 a month. Most
  people never reach the line and it can be declined, or dropped later
  by deleting photos.
- A printed seasonal planner posted out each January is 6.00. Entirely
  optional; the same thing is in the app for nothing.

The checkout is where the first two get added. Several beta users have
said the price on the page is not the price they were asked for.

## Constraints we already know about

- UK only for now. Everyone is a consumer.
- Turnover is nowhere near any tax threshold yet, but the accountant
  asked to be told before it is.
- Hosting cost per account has drifted up all year and there is no sign
  of it stopping. The image storage line is the one moving.
- One person runs this. Anything that needs a second pair of hands every
  month will not happen.

## Open

- Whether there are tiers at all, or one plan.
- Whether there is a trial, and how long.
- What we do when the cost per account keeps climbing.
- What we owe people who are already on the beta.
