""" Tests for users of the application."""

from django.db import transaction
from django.db.utils import DataError
from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    "Test User model."
    def setUp(self):
        self.user = User.objects.create(
            name="Test user exception"
        )

    def test_max_length(self):
        """Test max_length values."""
        user = self.user
        with transaction.atomic():
            user.email = 'x'*255
            with self.assertRaises(DataError):
                user.save()

        with transaction.atomic():
            user.name = 'x'*46
            with self.assertRaises(DataError):
                user.save()

        with transaction.atomic():
            user.last_name = 'x'*46
            with self.assertRaises(DataError):
                user.save()
