"""In-memory stand-ins used by the tests.

Keeping these here rather than in the test files means the storefront
tests can use them too.
"""

import itertools


class FakeGateway:
    """Stands in for `gateway.HttpPaymentGateway`.

    Authorisation always succeeds. Every call is recorded on `calls` so
    a test can assert what was sent.
    """

    def __init__(self, api_key="test-key"):
        self._api_key = api_key
        self._counter = itertools.count(1)
        self.calls = []

    def authorise(self, amount_pence, card_token):
        self.calls.append((amount_pence, card_token))
        number = next(self._counter)
        return {
            "reference": "pay_test_%04d" % number,
            "status": "approved",
            "amount_pence": amount_pence,
            "auth_code": "AC%04d" % number,
        }
