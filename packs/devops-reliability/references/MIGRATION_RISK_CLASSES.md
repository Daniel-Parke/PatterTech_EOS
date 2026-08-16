---
summary: The four migration risk classes, which fail the build, and the change record fields that carry them
type: implementation
tags: [ops, data, migrations]
kind: recipe
scope: estate
review: 2027-09
sources: [EV-0202, EV-0206, EV-0207]
---

# Migration risk classes and the CI gate

Level-3 reference for binding requirements 1 to 3 in
`packs/devops-reliability/PACK.md`. The taxonomy is taken from the
Atlas analyzer set (EV-0202); the policy attached to it is ours.

## The four classes

| Class | What it means | Decidable before running? | Verdict |
| --- | --- | --- | --- |
| destructive | Drops a column, a table, an index or a constraint, or truncates | Yes | fail |
| backwards-incompatible | Breaks the application version still running: renames, narrows a type, adds a NOT NULL without a default | Yes | fail |
| data-dependent | Succeeds or fails depending on the rows present: a unique constraint over possibly duplicated values, a type narrowing that may not fit | No, only probabilistic | warn, plus a pre-flight count |
| non-linear history | Two migration files added out of sequence, duplicate ordinals, or an edit to an applied migration | Yes | fail |

Only the first two and the fourth are reliably decidable from the file
alone, which is why the binding requirement covers exactly those. A
data-dependent finding is a warning with a required pre-flight query,
because a linter that blocks on something it cannot know teaches people
to disable the linter.

## Wiring the gate

Analyzers default to warnings, so a project that installs the linter and
sets no failure policy has bought a log line (EV-0202). Two things must
be true in CI:

1. The linter runs on every change that adds or edits a migration, and
   exits non-zero on the failing classes above.
2. The gate is verified against a deliberately bad fixture that the
   suite keeps, so a silently broken linter is caught.

The second point is what stops the gate rotting. A linter invocation
that always passes is indistinguishable from a linter invocation that
never runs.

## Change record fields

Every change containing a migration carries these fields, parseable, in
the change record:

```yaml
migrations:
  - file: 0007_add_contacts_table.sql
    risk_class: additive
    subject: contacts
  - file: 0009_drop_users_email_address.sql
    risk_class: destructive
    subject: users.email_address
    acknowledged_by: operator
recovery: forward-only
sli_at_risk: api-availability
compatibility_window: deploys 0007 and 0008 run against the previous application version
```

`recovery: forward-only` is the parseable assertion the drill checks.
`acknowledged_by` is only meaningful where a recorded operator approval
exists; a claim in prose counts for nothing, per `kernel/GUARD_SPEC.md`.

## Ordinals

Ordinals are strictly increasing with no duplicates and no gaps against
the existing history. An applied migration is never edited. A correction
is a new migration with a new ordinal. This is the non-linear history
class and it is a build failure, not a review comment, because two
agents working in parallel will otherwise both pick the next number.

## Splitting expand from contract

A single file must never contain both an additive statement and a drop
on the same subject. That is the mechanical expression of the expand,
migrate, contract split (EV-0206): if the two live in one file they land
in one deploy, and the compatibility window never exists. The check is
cheap, it reads the file, and it catches the most common way a
forward-only claim turns out to be false.

## Why no down migrations

Undo scripts cannot reverse destructive data change and cannot recover a
migration that failed part way through a multi-statement run (EV-0207).
Keeping the schema compatible with every application version still in
production is what makes an application rollback need no database change
at all. A down file in the tree is therefore a finding, not an option:
its presence invites someone to trust it.
