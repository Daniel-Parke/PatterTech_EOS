# lifecycle

The mailing side. Four commands, agreed over a pint, none of them
written. The stubs exit non-zero on purpose: a script that pretends to
work is worse than one that is obviously missing.

Everything runs from the repository root with no arguments beyond the
ones listed, and no third-party packages. The host we deploy to has a
bare Python and nothing else on it.

## The commands

    python lifecycle/send.py <address>

Sends the welcome sequence to one address. Exits 0 when the message is
handed off, non-zero when it refuses. It must refuse an address we are
not allowed to mail.

    python lifecycle/unsubscribe.py post "<uri>"

Stands in for the one-click POST the mailbox provider makes, so the whole
thing is testable without running a web server in CI. Prints the status
code it would return. Exit 0 for a 2xx, non-zero for anything else.

    python lifecycle/preflight.py --zone <path>

Checks the sending domain against a zone file before a bulk send. Exit 0
when every gate passes. Each gate that fails gets its own exit code so
the failure names itself instead of reporting a generic red.
`lifecycle/dns/production.json` is the live zone as it stands today.

    python lifecycle/validate_contacts.py <path>

Checks a contact file. Exit 0 when every record is fit to mail, non-zero
when any is not.

## The list

`contacts.json` is the trade show list, converted from the spreadsheet
last week. The fields are whatever the spreadsheet had in it and are
almost certainly not what we need to keep.

## The drafts

`emails/` holds the three messages as plain drafts. They are body copy
only. Nobody has worked out the headers a real send needs.
