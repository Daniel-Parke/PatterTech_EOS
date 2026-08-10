"""Route one support ticket to a queue.

`classify(text)` is what the inbox worker calls. It reads the prompt
from prompt.txt, asks the model and hands back the queue it chose.
"""

from pathlib import Path

import stub_client

MODEL = "support-classifier-latest"
PROMPT_PATH = Path(__file__).resolve().parent / "prompt.txt"


def _prompt():
    return PROMPT_PATH.read_text(encoding="utf-8")


def classify(ticket_text):
    """Return {"label": str, "abstain": bool} for one ticket."""
    reply = stub_client.complete(MODEL, _prompt(), ticket_text)
    return {"label": reply["label"], "abstain": False}
