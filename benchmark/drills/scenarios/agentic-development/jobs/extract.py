"""Turn one transcript into one complaint record.

The model call goes out through whatever command the ops box has in
SUPPORT_MODEL_CMD, which reads a prompt on stdin and writes one JSON
object on stdout. Everything else in here is prompt and parsing.
"""

import json
import os
import subprocess

PROMPT = """You are reading one closed support conversation.

Return one JSON object and nothing else, with these keys:
  ticket_id      the id you are given below
  night          the export date you are given below
  area           one of: sync, export, notifications, accounts, billing
  severity       one of: low, medium, high
  summary        one sentence, the customer's problem in their terms
  quotes         a list of short verbatim quotes from the customer
  resolved       true if the conversation ended with the issue fixed

Ticket: {ticket}
Night: {night}

Transcript:
{transcript}
"""


def extract_complaint(ticket, transcript, night):
    prompt = PROMPT.format(ticket=ticket, night=night, transcript=transcript)
    raw = run_model(prompt)
    record = json.loads(raw)
    record["ticket_id"] = ticket
    record["night"] = night
    return record


def run_model(prompt):
    cmd = os.environ.get("SUPPORT_MODEL_CMD")
    if not cmd:
        raise RuntimeError("SUPPORT_MODEL_CMD is not set on this box")
    proc = subprocess.run(cmd, shell=True, input=prompt, capture_output=True,
                          text=True, encoding="utf-8", timeout=180)
    if proc.returncode != 0:
        raise RuntimeError("model call failed: %s" % proc.stderr.strip()[:200])
    return proc.stdout.strip()
