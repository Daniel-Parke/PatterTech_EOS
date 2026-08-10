# support-inbox

Where the week's Sightline support inbox lands, and where whoever is on
rota writes it up afterwards. Sightline is the reporting and export
product; there are sixty paying accounts on it.

## What is in here

- `inbox/` one file per conversation, numbered in the order they
  arrived. Dropped here by the helpdesk export. Treat it as read only:
  the export rewrites the whole folder each time it runs, so anything
  edited in there is lost.
- `customers.csv` the account list, exported from billing at the same
  time. It carries contact names and email addresses, so nothing copied
  out of it belongs in anything that leaves this repository. Use the
  account id.
- `export-manifest.json` what the export covered and the moment it was
  taken. That timestamp is the clock for the week: anything dated after
  it has not happened yet.
- `out/` where the week's write-ups go. Empty at the start of a week.
- `docs/` how support is run here, as far as it is written down.

## How the week runs

The person on rota reads the inbox top to bottom, decides what each
item is and where it goes, deals with anything that is on fire, and
then writes the week up for the Monday product meeting. Everything is
done by hand. There is no ticket system beyond the helpdesk, and the
helpdesk export only goes one way.

See `docs/rota.md` for who does it and `docs/reporting.md` for what the
monthly deck expects.
