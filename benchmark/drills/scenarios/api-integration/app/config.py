"""Settings, read from the environment with defaults for local work."""

import os

DEFAULT_PAGE_SIZE = int(os.environ.get("ORDERS_PAGE_SIZE", "25"))
MAX_PAGE_SIZE = 100

# The payment provider sends this back to us on every event. It has been
# the same string since the first release.
WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN", "dev-shared-token")

# The provider also signs every event with this. Nothing reads it yet.
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "dev-signing-secret")
