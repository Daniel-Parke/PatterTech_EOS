# Migrations

Plain SQL, one file per change, named `NNNN_what_it_does.sql`. The
ordinal is four digits and comes from the last one that was merged.

`python scripts/migrate.py` applies everything that has not been applied
yet and records it in `schema_migrations`. It never runs anything in
`rollback/`; those are the hand-written undo scripts, and running one is
a decision a person makes during an incident.
