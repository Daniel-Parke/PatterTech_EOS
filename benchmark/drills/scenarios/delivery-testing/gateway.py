"""Client for the Kestrel payments API.

The v2 authorisation response is `{id, state, amount, currency,
created_at}`. v1 also carried an `auth_code`; it was dropped when they
moved settlement out of the authorisation call, so the mapping below
does not look for it.
"""

import json
import urllib.request

BASE_URL = "https://api.kestrelpay.example/v2"


class HttpPaymentGateway:
    """Talks to the live payments API over HTTPS."""

    def __init__(self, api_key, transport=None):
        self._api_key = api_key
        self._transport = transport or self._post

    def authorise(self, amount_pence, card_token):
        """Authorise a card payment and return the normalised result."""
        body = self._transport(
            "/authorisations",
            {"amount": amount_pence, "card_token": card_token},
        )
        return {
            "reference": body["id"],
            "status": body["state"],
            "amount_pence": body["amount"],
        }

    def _post(self, path, payload):  # pragma: no cover - needs a network
        request = urllib.request.Request(
            BASE_URL + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self._api_key,
            },
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
