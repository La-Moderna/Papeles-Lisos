""" Tests for clients of the application."""

from clients.models import Agent, Balance

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase


class AgentTestCase(TestCase):
    "Test Agent model."
    def setUp(self):
        self.user = Agent.objects.create(
            representant="Test agent exception"
        )

    def test_max_length(self):
        """Test max_length values."""
        user = self.user
        with transaction.atomic():
            user.representant = 'x'*46
            with self.assertRaises(DataError):
                user.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        user = self.user

        with transaction.atomic():
            user.representant = None
            with self.assertRaises(IntegrityError):
                user.save()


class BalanceTestCase(TestCase):
    "Test Balance model."
    def setUp(self):
        self.user = Balance.objects.create(
            order_balance="Test balance exception"
        )

    def test_max_length(self):
        """Test max_length values."""
        user = self.user

        with transaction.atomic():
            user.order_balance = 'x'*46
            with self.assertRaises(DataError):
                user.save()

        with transaction.atomic():
            user.facture_balance = 'x'*46
            with self.assertRaises(DataError):
                user.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        user = self.user

        with transaction.atomic():
            user.order_balance = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.facture_balance = None
            with self.assertRaises(IntegrityError):
                user.save()
