# Sedge

Stock counting for independent shops, cafes and small kitchens. Walk
round with a phone, type what is on the shelf, close the count, get a
list of what to order.

## Layout

- `app/` the application. `app/counts.py` holds a count and its lines,
  `app/items.py` the item list, `app/web.py` the handful of routes.
- `tests/` what little there is.
- `request.md`, `personas.md`, `support_export.csv` and `metrics.json`
  are product notes and exports rather than anything the app reads.
  They ended up at the top level and nobody has moved them.

## Running it

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt
FLASK_APP=app.web flask run
```

Tests: `python -m pytest`.

## Where the notes came from

`support_export.csv` is the helpdesk export for the quarter, one row a
ticket, tagged by whoever answered it. The tags are the desk's own and
nobody has audited them.

`metrics.json` comes out of the analytics job. It is the trailing
window, not the quarter, so it does not line up with the ticket export.

`personas.md` was written for the website refresh.

`request.md` is the note from commercial that started the current
argument about what to do next.
