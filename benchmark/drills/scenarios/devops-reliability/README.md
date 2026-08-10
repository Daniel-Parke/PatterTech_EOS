# users-service

The service that owns user records for the signup flow. Small, boring,
and on the critical path, so changes to it are made carefully.

## Layout

- `app/` the service code. `app/users.py` is the only module that
  touches user rows; `app/flags.py` reads `config/flags.json`.
- `migrations/` plain SQL, applied in ordinal order by
  `scripts/migrate.py`. `migrations/rollback/` holds the hand-written
  undo scripts we run when a release has to be pulled.
- `slo/` the service level objective, in OpenSLO format. The dashboards
  are generated from it, so keep it valid.
- `deploy/rollout.json` the canary plan. `scripts/rollout.py` reads it
  and decides whether a canary step may be promoted. It can abort a
  rollout on its own if the plan declares `failure_conditions`; today it
  declares none, so promotion is a human running the script and reading
  the answer.
- `evidence/` where we keep the output of anything we want to be able to
  show an auditor later. Empty at the moment.

## Running it locally

```
export APP_DB=var/app.db
python scripts/migrate.py
python scripts/seed.py
python -m unittest discover -s tests -t .
```

`APP_DB` picks the SQLite file. Everything defaults to `var/app.db`.

## House rules

- One migration per deploy, and the deploy has to be releasable on its
  own. We have been bitten by a migration that only worked if the code
  in the same pull request went out at the same instant.
- Nothing goes to production without the dashboards being watched for
  the length of the canary.
- Flags in `config/flags.json` are meant to be short lived. Give each
  one an owner and a date, and delete it once it has served its purpose.
