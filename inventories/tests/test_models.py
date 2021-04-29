""" Tests for users of the application."""

from django.db import transaction
from django.db.utils import DataError
from django.test import TestCase

from inventories.models import Inventory
from inventories.models import Warehouse


class InventoryTestCase(TestCase):
    "Test Inventory model."
    def setUp(self):
        self.warehouse = Warehouse.objects.create(
            description="This is fortesting models"
        )
        self.inventory = Inventory.objects.create(
            stock='2000', warehouse=self.warehouse
        )

    def test_max_length(self):
        """Test max_length values."""
        inventory = self.inventory
        warehouse = self.warehouse
        with transaction.atomic():
            inventory.stock = 4.0*2550000000000
            with self.assertRaises(DataError):
                inventory.save()

        with transaction.atomic():
            inventory.warehouse = warehouse
            with self.assertRaises(DataError):
                inventory.save()
