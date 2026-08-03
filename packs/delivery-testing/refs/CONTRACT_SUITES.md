---
summary: How to build and run a contract suite that proves a double still matches the real thing
kind: recipe
scope: estate
sources: [EV-0184, EV-0186, EV-0187, EV-0091, EV-0193, EV-0093]
type: example
tags: [delivery, testing, arch]
---

# Contract suites, in practice

Reference material for binding requirement 3 in the pack body. Read
WG-DEL-005 first for which double to pick.

## The vocabulary, so the argument stays clear

Five kinds of double, and they are not interchangeable (EV-0184).

| Kind | What it does |
| --- | --- |
| Dummy | Fills a parameter slot and is never used |
| Stub | Returns canned answers for the call under test |
| Spy | A stub that records what it was called with |
| Mock | Carries pre-programmed expectations about calls |
| Fake | A working implementation with a production-unsuitable shortcut |

Only the fake has behaviour, so only the fake can be held to a
behavioural contract. A stub or a mock cannot drift, because it never
claimed to be anything.

## What a contract suite is

One set of cases, written once, run against every implementation of the
port: the fake, and the real client. The fidelity claim being tested is
that the same inputs give the same outputs and the same state changes
(EV-0187). If a case can only be expressed against one of the two, it
belongs in that implementation's own tests rather than in the contract.

```python
# tests/contract/test_tariff_port_contract.py
import pytest

from app.adapters.tariff_http import HttpTariffClient
from app.adapters.tariff_fake import FakeTariffClient

@pytest.fixture(params=["fake", "real"])
def client(request, recorded_responses):
    if request.param == "fake":
        return FakeTariffClient()
    return HttpTariffClient(transport=recorded_responses)

def test_unknown_tariff_code_raises_not_found(client):
    with pytest.raises(TariffNotFound):
        client.fetch("no-such-code")

def test_returned_rate_carries_no_legacy_unit_price_field(client):
    result = client.fetch("E7-STD")
    assert not hasattr(result, "unit_price")
```

Two properties matter more than the style. Both implementations reach
the same assertions from the same parameterisation, and the assertions
name behaviour rather than internals.

Put the file under `tests/contract/` and name it after the port it
covers, so both a reviewer and a checker can find it without being
told where to look.

## Where the real side comes from

- **A reachable test instance.** Best, and rare for third parties.
- **Recorded real responses**, captured from the live service and
  replayed into the real client. This is what makes the suite runnable
  in CI without network access. The recording carries a capture date
  and is refreshed on the same cadence as the contract run.
- **A container running the real software** for infrastructure, where
  the real thing is a database or a broker rather than a service
  (EV-0093).

A recording that nobody refreshes is a second thing that drifts. Put
its refresh in the cadence, not in someone's memory.

## Cadence and disposition

- The fake runs in the fast suite, every commit.
- The contract suite runs on a stated slower cadence, nightly or before
  release, against the real side (EV-0186).
- **Services we own**: the verification result answers the deploy
  question by exit code, and what actually shipped is written back so
  the next answer is asked against reality rather than a wiki page
  (EV-0193, EV-0091).
- **Services we do not own**: the contract runs as a monitor. A red
  result opens an investigation and updates the fake; it does not block
  a merge nobody can unblock (EV-0186).

## What a contract suite does not catch

- Semantic drift inside a stable shape. The field is still there and
  now means something else.
- Emergent behaviour of the assembled system (EV-0091).
- Anything the recorded interactions never covered.
- A stale deploy matrix, when something shipped outside the pipeline
  and the gate went green on out-of-date facts (EV-0193).

## Drift smells

- A fake nobody has touched since the integration landed.
- A fake that returns a field the real client stopped returning, or
  that never learned about a field the real client added.
- Contract cases that exist only for the fake.
- A recording with no capture date.
- A fake written by us for a service that ships its own.
