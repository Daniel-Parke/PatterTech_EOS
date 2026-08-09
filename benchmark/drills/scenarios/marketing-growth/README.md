# kilnwatch

Firing logs and kiln schedules for studio potters. Two of us, part time,
launching in the autumn.

## Layout

- `site/` the static marketing site. Plain HTML, no build step. Deployed
  by copying the folder onto the host, so whatever is in here is what is
  live.
- `lifecycle/` the mailing side. Almost none of it is written yet. The
  intended commands are in `lifecycle/README.md`; the scripts are stubs
  that exit non-zero so nobody mistakes them for working.
- `notes/` rough working notes. Not published.

## Running it

    make serve      # serves site/ on localhost:8000
    make check      # placeholder, checks nothing yet

## Known state

The site went up in a hurry for a trade show. Things we know are wrong:

- `site/robots.txt` still carries the staging rule that hides the whole
  site. It has been like that since June.
- `site/sitemap.xml` was written by hand and has not kept up with the
  pages.
- The structured data on the home and pricing pages was copied off
  another site and edited badly.
- `lifecycle/contacts.json` is the list from the trade show, kept in a
  spreadsheet until last week. Nobody has checked what we are allowed to
  send to whom.
