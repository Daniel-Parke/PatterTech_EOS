"""sigcheck: request signatures, the boring correct way."""

import hashlib
import hmac

__version__ = "0.7.3"


def sign(payload, secret):
    """Hex HMAC-SHA256 of payload under secret."""
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    if isinstance(secret, str):
        secret = secret.encode("utf-8")
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def verify(payload, secret, given):
    return hmac.compare_digest(sign(payload, secret), given or "")
