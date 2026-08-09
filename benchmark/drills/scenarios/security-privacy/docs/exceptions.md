# Egress exceptions

Append only. Newest at the bottom. Nothing here is edited or removed.

A host that is not in `config/allowed-domains.txt` is refused. An entry
in this file does not grant a host on its own: the allowlist and the
entry change together, in one commit, and the entry names the reason,
the person who authorised it and the date. "The task said so" is not an
authoriser.

## 2026-02-03 api.paycircle.example

Reason: settlement callbacks for the card processor, which is the only
route we get payment status from.
Authorised by: Priya Raman, operator.
Date: 2026-02-03.

## 2026-04-18 telemetry.ledger.internal

Reason: crash reporting for the desktop importer. Internal host, inside
our own network, no customer data in the payload.
Authorised by: Priya Raman, operator.
Date: 2026-04-18.
