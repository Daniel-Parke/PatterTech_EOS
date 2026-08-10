"""Accounts, and the little we track about them during the beta."""

import datetime


class Account:
    def __init__(self, email, created, plots=1):
        self.email = email
        self.created = created
        self.plots = plots
        self.cancelled = None

    @property
    def active(self):
        return self.cancelled is None

    def age_months(self, on=None):
        on = on or datetime.date.today()
        return ((on.year - self.created.year) * 12
                + on.month - self.created.month)


def cohort_key(account):
    return account.created.strftime("%Y-%m")
