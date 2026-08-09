"""Settings, read once at start up.

Values come from `postbox.conf` on the box and fall back to what is
here, which is what the local runs use.
"""

import os
from pathlib import Path

import duraconf

DEFAULTS = {
    "site_name": "Postbox",
    "data_dir": "data",
    "export_secret": "local-only-not-a-secret",
    "support_address": "hello@postbox.example",
}

CONF_PATH = Path(os.environ.get("POSTBOX_CONF", "/etc/postbox/postbox.conf"))


def load(path=None):
    """Settings for this process. Missing file means defaults."""
    path = Path(path) if path else CONF_PATH
    settings = dict(DEFAULTS)
    if path.is_file():
        settings.update(duraconf.read(path))
    return settings


def data_dir(settings=None):
    settings = settings or load()
    return Path(settings["data_dir"])
