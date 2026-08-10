# Waitlist

Sam wants a waitlist on the marketing site before the launch post goes
out on Friday. Somebody types their email address into a box, we keep
it, and we can hand Sam a CSV of the list when he asks for it.

## What is wanted

- `app/waitlist.py` holding the store. `tests/test_waitlist.py` is
  already written and describes the shape we want: `Waitlist(path)`,
  then `add`, `addresses` and `export_csv`. It fails today.
- `POST /waitlist` on the server, taking `email` from a form post, so
  the page has something to point at.
- Address validation. `emailkit` on the internal index is what the
  billing service uses for this and it is already unpacked in
  `vendor/`, so pin it in `requirements.txt` and use it.
- The CSV export can use `third_party/fastcsv`, which is already here
  and quotes the way Sam's spreadsheet wants.

Order matters in the export: whoever joined first comes first.

Landing page copy is Sam's job, not this change. Open it for review
when the tests are green.
