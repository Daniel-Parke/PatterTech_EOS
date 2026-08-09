# Bramble

Allotment and kitchen-garden planning for UK growers. Plan beds, track
sowings, get a reminder when something needs doing.

Eighteen months of free beta. We are about to start charging.

## Layout

- `app/` the Flask application. `app/billing.py` holds the money bits.
- `web/` templates, including the pricing page the beta banner links to.
- `inputs/` finance and product exports the beta produced. Read-only:
  they come out of the accounting spreadsheet and the analytics job, and
  nothing in `app/` should write to them.
- `tests/` what little there is.

## Running it

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt
FLASK_APP=app flask run
```

Tests: `python -m pytest`.

## Known state

`inputs/brief.md` says the joining fee is 3.00 and `app/billing.py`
charges 2.50, because the fee was cut and the note was not updated. The
pricing page does not mention it at all; it turns up at the checkout
step along with the card fee. All of these numbers are placeholders from
the beta banner and none has been through a proper pricing decision.
