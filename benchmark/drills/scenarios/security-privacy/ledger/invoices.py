"""The invoice record and the status filters over it."""

from __future__ import annotations

from dataclasses import dataclass

DRAFT = "draft"
SETTLED = "settled"
VOID = "void"

STATUSES = (DRAFT, SETTLED, VOID)


@dataclass(frozen=True)
class Invoice:
    """One invoice. Totals are integers in pence, never floats."""

    number: str
    customer: str
    status: str
    total_pence: int
    settled_on: str = ""

    def __post_init__(self):
        if self.status not in STATUSES:
            raise ValueError("unknown status: %r" % self.status)
        if not isinstance(self.total_pence, int):
            raise TypeError("totals are integers in pence")


def settled(invoices):
    """Every settled invoice, in the order given."""
    return [i for i in invoices if i.status == SETTLED]


def total_pence(invoices):
    return sum(i.total_pence for i in invoices)
