""" Tests for clients of the application."""
from clients.models import Agent, Balance, Client

from companies.models import Company

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase, client

from inventories.models import Warehouse


class AgentTestCase(TestCase):
    "Test Agent model."

    def setUp(self):
        self.company = Company.objects.create(
            company_id='619',
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
        self.agent = Agent.objects.create(
            representant="edmond",
            company=self.company
        )

        self.warehouse = Warehouse.objects.create(
                name="21b",
                description="This is a test",
                company=self.company
        )

        self.client = Client.objects.create(
                client_id="1212",
                company=self.company,
                nameA="Manuel",
                nameB="Urgell",
                status=1,
                agent=self.agent,
                analist="Analises",
                currency="MXN",
                credit_lim=2000,
                warehouse=self.warehouse
        )
        self.user = Balance.objects.create(
            order_balance="1400",
            facture_balance="1500",
            client=self.client,
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
            client.client_id = 'x'*11
            with self.assertRaises(DataError):
                user.save()

        with transaction.atomic():
            company.id = 'x'*5
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

        with transaction.atomic():
            user.client = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.company = None
            with self.assertRaises(IntegrityError):
                user.save()
