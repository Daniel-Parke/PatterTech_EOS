"""A stock count and the lines in it."""

from dataclasses import dataclass, field


class CountClosed(Exception):
    """Raised when a closed count is written to."""


@dataclass
class Line:
    item_id: str
    quantity: float
    unit: str
    entered_by: str


@dataclass
class Count:
    count_id: str
    site: str
    area: str
    opened_by: str
    lines: dict = field(default_factory=dict)
    closed: bool = False

    def enter(self, item_id, quantity, unit, entered_by):
        """Record a quantity against an item.

        Entering the same item twice replaces the earlier line. The last
        person to type wins, which is how the desk describes it too.
        """
        if self.closed:
            raise CountClosed(self.count_id)
        self.lines[item_id] = Line(item_id, quantity, unit, entered_by)
        return self.lines[item_id]

    def close(self):
        self.closed = True
        return self

    def reopen(self):
        self.closed = False
        return self

    def total_lines(self):
        return len(self.lines)

    def missing(self, item_ids):
        """Items on the list that nobody entered a quantity for."""
        return [i for i in item_ids if i not in self.lines]


def summarise(count, catalogue):
    """Value a count against the catalogue, ignoring unpriced items."""
    total = 0.0
    for line in count.lines.values():
        item = catalogue.get(line.item_id)
        if item is None or item.unit_cost is None:
            continue
        total += line.quantity * item.unit_cost
    return total
