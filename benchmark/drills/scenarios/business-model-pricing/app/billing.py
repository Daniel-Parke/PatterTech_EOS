"""Money. Placeholder numbers from the beta banner.

Everything in here is in pence, because floats and money do not mix.
"""

PLAN_PENCE = 599
JOINING_FEE_PENCE = 250
PROCESSING_FEE_PENCE = 49
EXTRA_STORAGE_PENCE = 200
PRINTED_PLANNER_PENCE = 600


def first_payment_pence(extra_storage=False):
    total = PLAN_PENCE + JOINING_FEE_PENCE + PROCESSING_FEE_PENCE
    if extra_storage:
        total += EXTRA_STORAGE_PENCE
    return total


def recurring_payment_pence(extra_storage=False):
    total = PLAN_PENCE + PROCESSING_FEE_PENCE
    if extra_storage:
        total += EXTRA_STORAGE_PENCE
    return total


def format_gbp(pence):
    return "£%d.%02d" % divmod(pence, 100)
