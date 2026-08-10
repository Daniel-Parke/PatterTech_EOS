---
summary: Worked example, an auth change routed R3 end to end, oracle first, reviewer and operator at the gate
type: example
tags: [eos]
---

# Worked example: the high-assurance run

The same kernel as examples/v2-worked-lean.md, at the other end of the
dial. The venture is FieldKit, the ORG seed at
benchmark/fixtures/seed-v2-ORG, a real compiled seed in this repository
that passes the seed check with zero errors. FieldKit is an internal
field-survey app: surveyors sign in on a phone, the office exports CSV,
and the login email is the only personal data it holds. The fixture is
the seed as compiled, with no code in it yet, so the scene below is set
after FieldKit's first delivery sprint; paths starting org/ or tests/
are the venture's own.

## The request

Surveyors are being logged out mid-survey and losing entered data. The
fix is a session model change: shorter access tokens with rotation, a
refresh path, and a one-off revocation of every session that exists
today so nobody is left holding a token minted under the old rules.
Users get one notice email explaining the sign-in they will hit.

## Declared facts

The owner opens a task record under the venture's org/tasks/ directory,
per kernel/schemas/task-record.schema.json, and declares before it
routes:

```json
{
  "capabilities": ["database", "network"],
  "side_effects": ["touches-auth", "irreversible-action", "sends-external"]
}
```

Three declarations, each true and each with a reason. Auth, because the
session model is the auth surface. Irreversible, because a revoked
session cannot be un-revoked; every surveyor in the field signs in
again and there is no undo. External, because the notice email leaves
the system.

## The ruling

```json
{
 "tier": "R3",
 "reasons": [
  {"factor": "irreversible-action", "tier_floor": "R3", "source": "declared",
   "evidence": "declared side effect: irreversible-action"},
  {"factor": "auth-surface", "tier_floor": "R2", "source": "declared",
   "evidence": "declared side effect: touches-auth"},
  {"factor": "boundary-contact", "tier_floor": "R1", "source": "declared",
   "evidence": "declared side effect: sends-external"}
 ],
 "discrepancies": []
}
```

Three active factors, three floors, and the highest wins. Auth alone
would have ruled R2; the revocation is what takes it to R3, and the
external send denies Express without raising anything by itself. Each
reason names the factor, its floor, whether the signal was declared or
derived, and the evidence, so the ruling audits later without anyone's
memory.

Discrepancies is empty because the declaration matched what the diff
later exposed. Had the owner left out the auth declaration, the derived
signals would have activated the factor anyway and marked the row a
discrepancy, and nothing would have merged until the task was
re-declared and re-routed. Honest declaration costs nothing.

R3 is High-assurance plus a human, per kernel/POLICY_SPEC.md.

## Phase 1 · The oracle, before any implementation

A separate ORACLE session writes the gate tests first, holding no
implementation in context. That separation is the one v1 rule v2 kept
whole, and the reason is measured: tests written after seeing the code
catch roughly half as many faults. The charter is
benchmark/fixtures/seed-v2-ORG/org/roles/ORACLE.md and the argument is
`packs/delivery-testing/guides/WG-DEL-006-oracle-independence.md`.

The independence method is property-based rather than the clean-context
default, because auth invariants state better as properties than as
cases. Three of them:

- No token minted before the revocation timestamp authenticates after
  it, for any user, any role, any endpoint.
- Rotation never widens a session: the new token's expiry is never
  later than the old session's absolute deadline.
- A refresh presented twice fails the second time, and the failure
  revokes the whole chain.

The oracle is frozen on the task record before implementation starts:

```json
"oracle_provenance": {
  "files": ["tests/auth/test_session_properties.py",
            "tests/auth/test_revocation_boundary.py"],
  "hashes": {"tests/auth/test_session_properties.py": "sha256 at freeze",
             "tests/auth/test_revocation_boundary.py": "sha256 at freeze"},
  "author_session": "S-0031",
  "independence_method": "property-based"
}
```

The hashes are shown illustratively here; in a real record they are
full digests, and the checker verifies the gates still match them.

## Phase 2 · The implementer

A different session takes the EXECUTOR charter, claims the auth module
and the migration directory, and works to the frozen oracle. Two rules
bite hard here.

The oracle is not the implementer's to change. Property two turned out
awkward, because the old model had no absolute deadline to compare
against. The implementer requested an amendment and did not write one;
the ORACLE session authored it as an append-only entry carrying reason,
change, old hash, new hash and the operator's authorisation, because at
R3 the operator authorises amendments. The original stays on the
record, and amendment frequency surfaces at retro as an oracle-quality
signal.

The rollback plan is written before the change ships: the migration is
additive, the old validation path stays behind a flag for one release,
and the revocation runs as a separate step so the code can ship without
it.

## Phase 3 · Acceptance

A REVIEWER session owning none of the implementation reviews at
acceptance, per benchmark/fixtures/seed-v2-ORG/org/roles/REVIEWER.md.
It may repair trivia in non-gate artefacts and may never touch a test
or a check. Its verdict is one row on the task record: role, session,
verdict, date, a short note. Ten lines is the budget and it is enough.

Then the operator approves, because R3 always ends at a human for
anything irreversible. That approval is a recorded event rather than a
sentence in a transcript.

## Phase 4 · The one external action

The notice email is a consequential external action, so the guard
evaluates it immediately before execution, independently of the tier
that has already been ruled:

```json
{
 "action_class": "external-write",
 "payload_summary": "send the one-off sign-in notice to every FieldKit user through the transactional email provider",
 "verdict": "manual-only",
 "reasons": [
  "non-waivable floor new-external-destination: manual-only",
  "fail closed: no validated host enforcement adapter"
 ],
 "adapter_validated": false,
 "floor_hit": "new-external-destination"
}
```

Two independent reasons, either decisive alone. Publishing to a new
external destination is a non-waivable floor in kernel/GUARD_SPEC.md,
which no reviewer, capability profile, exception or emergency overlay
can lower. And FieldKit's policy carries guard validated false, so with
no validated enforcement adapter every guarded class is manual-only
anyway.

Manual-only does not mean blocked. It means the agent cannot perform it
under any approval, so the agent drafts the copy, the operator presses
send, and the task record says which of the two happened. Naming a host
permission system would not have satisfied this; only a shipped mapping
proven by the bypass suite does.

## What exists at the end

A task record with declared facts, the ruling and its reasons, the
frozen oracle with its one amendment, the rollback plan, the reviewer
verdict and the operator approval. The commits. The tests. Nothing
else: no session log, no Resume Packet, no status document whose only
content is that another document changed.

## What would have lowered it

Letting old tokens expire naturally instead of revoking them removes
the irreversible factor, and the ruling falls to R2: oracle and
independent review kept, mandatory human lost. Shipping without the
notice email removes the external action and the guard never runs.
Neither is a trick, because the tier followed the facts both times.

An exception cannot buy the same reduction. A downward move needs
concrete evidence and an authoriser, lands on the task record beside
the ruling it lowers, and gets sampled at retro. Nothing on that path
crosses a non-waivable floor.
