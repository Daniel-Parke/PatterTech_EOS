"""A list of records in a JSON file.

Our volumes are tiny and a database would be one more thing to run. If
that stops being true this is the file to replace.
"""

import json
from pathlib import Path


class JsonList:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        """Every record, oldest first. A missing file reads as empty."""
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        try:
            rows = json.loads(text)
        except ValueError:
            return []
        return rows if isinstance(rows, list) else []

    def write(self, rows):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(list(rows), indent=1) + "\n",
                       encoding="utf-8")
        tmp.replace(self.path)

    def append(self, row):
        rows = self.read()
        rows.append(row)
        self.write(rows)
        return row
