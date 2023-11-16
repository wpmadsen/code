from django.test import TestCase

from libcal_bookings import models  # noqa: F401


class ModelTests(TestCase):
    def setUp(self):
        """
        Create models for testing.
        """
        pass

    def tearDown(self):
        """
        Remove models. Clean up.
        """
        pass

    def test_nothing(self):
        """
        Sample test.
        """
        self.assertEqual(2, 1 + 1)
