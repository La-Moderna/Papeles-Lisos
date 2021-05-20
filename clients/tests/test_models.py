""" Tests for clients of the application."""
from clients.models import Agent, Balance

from companies.models import Company

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase


class AgentTestCase(TestCase):
    "Test Agent model."

    def setUp(self):
        self.company = Company.objects.create(
            id='619',
            name="Ejemplo1"
        )
        self.user = Agent.objects.create(
            representant="Test agent exception",
            company=self.company
        )

    def test_max_length(self):
        """Test max_length values."""
        user = self.user
        with transaction.atomic():
            user.representant = 'x'*46
            with self.assertRaises(DataError):
                user.save()

        company = self.company
        with transaction.atomic():
            company.id = 'x'*5
            with self.assertRaises(DataError):
                user.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        user = self.user

        with transaction.atomic():
            user.representant = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            Company.id = None
            with self.assertRaises(IntegrityError):
                user.save()


class BalanceTestCase(TestCase):
    "Test Balance model."
    def setUp(self):
        self.company = Company.objects.create(
            id='619',
            name="Ejemplo1"
        )
        self.user = Balance.objects.create(
            order_balance="1400",
            facture_balance="1500",
            company=self.company
        )

    def test_max_length(self):
        """Test max_length values."""
        user = self.user
        company = self.company

        with transaction.atomic():
            user.order_balance = 'x'*46
            with self.assertRaises(DataError):
                user.save()

        with transaction.atomic():
            user.facture_balance = 'x'*46
            with self.assertRaises(DataError):
                user.save()

        with transaction.atomic():
            company.id = 'x'*5
            with self.assertRaises(DataError):
                user.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        user = self.user
        company = self.company

        with transaction.atomic():
            user.order_balance = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.facture_balance = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            company.id = None
            company.save()
            with self.assertRaises(IntegrityError):
                user.save()
