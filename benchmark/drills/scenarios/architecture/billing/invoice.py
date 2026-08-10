"""Invoice totals. The price lookup the drill asks for does not exist yet."""

from shared import money


def total(line_amounts):
    return money.format_gbp(sum(line_amounts))
