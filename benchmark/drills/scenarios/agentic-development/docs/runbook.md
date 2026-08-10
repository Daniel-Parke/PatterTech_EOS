# Runbook

## The nightly run

Cron on the ops box, in the deploy user's crontab:

    25 3 * * * cd /srv/support-digest && python jobs/nightly.py $(date -d yesterday +\%F) >> /var/log/support-digest.log 2>&1

It starts after the helpdesk export lands at 03:10 and usually finishes
around 04:15. Forty transcripts, one at a time, one model call each.

## When it stops halfway

There is no resume. The log tells you which ticket it reached, and
`state/complaints.jsonl` has everything up to that point, but the
runner has no idea any of that happened. Restarting it re-does the
whole night and writes every record a second time, so the file has to
be trimmed by hand first.

This has happened three times since April: twice a reboot for patching,
once the model command timed out and took the process with it.

## The weekly report

Thursday morning, whoever is on rota:

1. `python tools/validate_complaints.py state/complaints.jsonl`
2. Read the week's records, group them by area, write
   `reports/<iso-week>.md` in the same shape as last week's.
3. Open a pull request against `main` with the report, tag the product
   lead for review.

Step 2 takes about an hour and a half and is the reason nobody wants
the rota. Step 3 is the only thing anyone outside the team sees, so it
has never gone out without someone reading it first.
