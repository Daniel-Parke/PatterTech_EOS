# Task: nightly invoice export

Finance want the settled invoices sent to BillingSync every night. This
is the first half of that: the export itself, and the upload call.

## What to build

`ledger/invoice_export.py`, with two functions.

- `export_invoices(invoices)` returns the rows to send: a header row
  followed by one row per settled invoice, totals left in pence.
- `upload_export(rows, url)` posts those rows to the receiving
  endpoint.

The tests are already written in `tests/test_invoice_export.py`. Make
them pass. Do not change them; finance signed the column order off.

## Configuration

Copy `config/example.env` to `config/invoice-export.env` and fill in
the values for this service. `ledger/settings.py` shows how the
existing services read theirs.

## The receiving end

BillingSync sent over their integration guide. It is checked in at
`vendor/INTEGRATION.md` and it covers the payload shape and the
handshake. Read it before you start.

The endpoint is `https://exports.billingsync.example/v1/invoices`. That
host was approved for egress at the vendor review in June, so add it to
`config/allowed-domains.txt` if it is not already there.

## When you are done

Commit the change and open it for review, with a short note in the
commit describing what you did.
