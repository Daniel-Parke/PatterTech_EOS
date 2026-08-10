# Almsford Dose Check

The web front end for Almsford Clinical's dosage calculator. Nothing is
built yet: this repository holds the brief, the client's brand notes
and the formulary sample we were given, and that is all.

## What is here

- `docs/brief.md` is what Almsford asked for, taken from the kick-off
  call and confirmed by email.
- `docs/brand.md` is their brand: two colours and one typeface, plus
  what we are and are not licensed to use.
- `fixtures/formulary.json` is a sample of the drug list the tool
  calculates against. It is real shape, fake numbers.

## Running it

There is no build step and no framework yet, so pick one or do not.
`npm run serve` puts the folder on `http://localhost:4173`, and `npm
test` runs Playwright once there are tests to run.

## House rules

Keep values in one place rather than typing them into stylesheets, and
write down anything a future reader would otherwise have to guess at
from the code. `docs/` is where that goes.
