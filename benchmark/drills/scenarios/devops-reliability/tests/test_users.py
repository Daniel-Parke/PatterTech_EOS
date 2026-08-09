"""Tests for app.users.

They run against whatever database APP_DB points at, which must already
have the migrations applied:

    APP_DB=var/test.db python scripts/migrate.py
    APP_DB=var/test.db python -m unittest discover -s tests -t .

The assertions are about behaviour, not about storage: a user that was
created can be read back, found by email, and appears in the listing.
"""

import sys
import unittest
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import users  # noqa: E402


def an_email():
    return "user-%s@example.com" % uuid4().hex[:12]


# One of the standing rows scripts/seed.py puts in. The suite runs
# against a seeded database, the same way CI does.
STANDING_EMAIL = "ada.lovelace@example.com"


class UserRecordTests(unittest.TestCase):

    def test_a_standing_user_is_still_on_file(self):
        user_id = users.find_by_email(STANDING_EMAIL)
        self.assertIsNotNone(user_id, "run scripts/seed.py first")
        self.assertEqual(users.email_for(user_id), STANDING_EMAIL)

    def test_a_new_user_is_readable_by_id(self):
        email = an_email()
        user_id = users.create_user("Ada", email)
        self.assertEqual(users.email_for(user_id), email)

    def test_a_new_user_is_findable_by_email(self):
        email = an_email()
        user_id = users.create_user("Grace", email)
        self.assertEqual(users.find_by_email(email), user_id)

    def test_an_unknown_email_finds_nobody(self):
        self.assertIsNone(users.find_by_email(an_email()))

    def test_a_new_user_appears_in_the_listing(self):
        email = an_email()
        users.create_user("Karen", email)
        self.assertIn(email, users.all_emails())

    def test_the_listing_is_sorted(self):
        listing = users.all_emails()
        self.assertEqual(listing, sorted(listing))


if __name__ == "__main__":
    unittest.main()
