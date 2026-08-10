import json
from pathlib import Path

from gateway import HttpPaymentGateway

RECORDED = json.loads(
    (Path(__file__).parent / "data" / "kestrel_authorisation.json")
    .read_text(encoding="utf-8")
)


def _transport(path, payload):
    assert path == "/authorisations"
    assert payload["amount"] == RECORDED["amount"]
    return RECORDED


def test_authorise_maps_the_v2_response():
    gateway = HttpPaymentGateway("test-key", transport=_transport)
    result = gateway.authorise(RECORDED["amount"], "tok_live_4h2")
    assert result == {
        "reference": "pay_9f2c41",
        "status": "approved",
        "amount_pence": 1250,
    }
