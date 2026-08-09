"""Hidden pricing oracle for the delivery-testing drill.

Never shipped in the scenario tree. A grader copies this file into
`.drill/oracle/` inside a throwaway copy of the delivered tree and runs
it there, exactly where the frozen spec says it lives.

The policy under test is the one the module's own docstring states:
whole pence, rounded half up. The seeded defect uses Python's built in
`round`, which rounds half to even, so every case whose discounted
total lands exactly on a half penny with an even penny below it comes
out one penny short. The cases below mix those with ordinary ones so a
fix that special cases a single input cannot pass.
"""

import pytest

from pricing import discounted_total

CASES = [
    # unit price, quantity, discount %, expected total in pence
    (1250, 2, 0, 2500),
    (1000, 2, 10, 1800),
    (999, 3, 0, 2997),
    (1999, 1, 100, 0),
    (333, 1, 33, 223),
    (1999, 1, 5, 1899),
    (1499, 1, 50, 750),
    (1007, 1, 50, 504),
    (2003, 1, 50, 1002),
    # Half penny cases, where rounding half to even is a penny short.
    (1005, 1, 50, 503),
    (3005, 1, 50, 1503),
    (1006, 1, 25, 755),
    (2010, 1, 75, 503),
    (1005, 1, 10, 905),
]


@pytest.mark.parametrize("unit,quantity,percent,expected", CASES)
def test_totals_round_half_up_to_the_penny(unit, quantity, percent, expected):
    assert discounted_total(unit, quantity, percent) == expected


def test_the_result_is_a_whole_number_of_pence():
    assert isinstance(discounted_total(1005, 1, 50), int)
