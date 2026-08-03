"""Entry point: python -m tools.eos <cmd>."""

import sys

from .cli import main

sys.exit(main())
