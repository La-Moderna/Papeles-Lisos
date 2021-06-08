""" Tests for users of the application."""

from companies.models import Company

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from inventories.models import Inventory
from inventories.models import Item
from inventories.models import Warehouse


class InventoryTestCase(TestCase):
    "Test Inventory model."
    def setUp(self):

        self.company = Company.objects.create(
            company_id='222',
            name="Ejemplo 1"
        )
        self.warehouse = Warehouse.objects.create(
            description="Test warehouse exception",
            company=self.company
        )
        self.item = Item.objects.create(
            item_id="10015474",
            description="61200005001",
            udVta="MIL",
            access_key="864",
            standar_cost=2.0583,
            company=self.company
        )
        self.inventory = Inventory.objects.create(
            stock='2000',
            warehouse=self.warehouse,
            item=self.item
        )

    def test_max_length(self):
        """Test max_length values."""
        inventory = self.inventory
        with transaction.atomic():
            inventory.stock = 4.0*2550000000000
            with self.assertRaises(DataError):
                inventory.save()

        with transaction.atomic():
            inventory.warehouse.description = 'x'*101
            with self.assertRaises(DataError):
                inventory.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        inventory = self.inventory

        with transaction.atomic():
            inventory.warehouse = None
            with self.assertRaises(IntegrityError):
                inventory.save()

        with transaction.atomic():
            inventory.item = None
            with self.assertRaises(IntegrityError):
                inventory.save()

    def test_on_delete_inventory_fk_warehouse(self):
        """Test on delete constraints (DELETE ON CASCADE)"""
        company_test = Company.objects.create(
            company_id='com1',
            name='Papeles de prueba')
        item_test = Item.objects.create(
            item_id='asc45g',
            description='This is for testing delete of objects',
            udVta='cue2',
            access_key='acess345j',
            standar_cost=123.4345,
            company=company_test)

        warehouse_1 = Warehouse.objects.create(
            name='tes7',
            description='this is a test',
            company=company_test)

        inventory = Inventory.objects.create(
            stock=3000,
            warehouse=warehouse_1,
            item=item_test)

        warehouse_1.delete()
        inventory_qs = Inventory.objects.filter(pk=inventory.pk)
        self.assertEqual(inventory_qs.exists(), False)
        inventory_qs.delete()

    def test_on_delete_inventory_fk_item(self):
        """Test on delete constraints (DELETE ON CASCADE)"""
        company_test = Company.objects.create(
            company_id='com1',
            name='Papeles de prueba')
        item_test = Item.objects.create(
            item_id='asc45g',
            description='This is for testing delete of objects',
            udVta='cue2',
            access_key='acess345j',
            standar_cost=123.4345,
            company=company_test)

        warehouse_1 = Warehouse.objects.create(
            name='tes7',
            description='this is a test',
            company=company_test)

        inventory = Inventory.objects.create(
            stock=3000,
            warehouse=warehouse_1,
            item=item_test)

        item_test.delete()
        inventory_qs = Inventory.objects.filter(pk=inventory.pk)
        self.assertEqual(inventory_qs.exists(), False)
        inventory_qs.delete()


class WarehouseTestCase(TestCase):
    """Test warehouse model"""

    def setUp(self):

        self.company = Company.objects.create(
            company_id='222',
            name="Ejemplo 1"
        )
        self.warehouse = Warehouse.objects.create(
            description="Test warehouse exception",
            company=self.company
        )
        self.item = Item.objects.create(
            item_id="10015474",
            description="61200005001",
            udVta="MIL",
            access_key="864",
            standar_cost=2.0583,
            company=self.company
        )
        self.inventory = Inventory.objects.create(
            stock='2000',
            warehouse=self.warehouse,
            item=self.item
        )

    def test_max_length(self):
        warehouse = self.warehouse
        with transaction.atomic():
            warehouse.name = 'x'*10
            with self.assertRaises(DataError):
                warehouse.save()

        with transaction.atomic():
            warehouse.description = 'x'*101
            with self.assertRaises(DataError):
                warehouse.save()

    def test_nulls(self):
        warehouse = self.warehouse
        with transaction.atomic():
            warehouse.description = None
            with self.assertRaises(IntegrityError):
                warehouse.save()

        with transaction.atomic():
            warehouse.name = None
            with self.assertRaises(IntegrityError):
                warehouse.save()

        with transaction.atomic():
            warehouse.company = None
            with self.assertRaises(IntegrityError):
                warehouse.save()

    def test_on_delete_warehouse_fk(self):
        """Test on delete constraints (DELETE ON CASCADE)"""
        company_test = Company.objects.create(
            company_id='com1',
            name='Papeles de prueba')

        warehouse_1 = Warehouse.objects.create(
            name='tes7',
            description='this is a test',
            company=company_test)

        company_test.delete()
        warehouse_qs = Warehouse.objects.filter(pk=warehouse_1.pk)
        self.assertEqual(warehouse_qs.exists(), False)
        warehouse_qs.delete()


class ItemTestModels(TestCase):
    """Test Item Model"""

    def setUp(self):
        """Create initial values"""

        self.company = Company.objects.create(
            company_id="222",
            name="Papeles de Toluca"
        )

        self.item = Item.objects.create(
            item_id="10015474",
            description="61200005001",
            udVta="MIL",
            access_key="864",
            standar_cost=2.0583,
            company=self.company
        )

    def test_max_length(self):

        item = self.item

        with transaction.atomic():
            item.item_id = 'x' * 21
            with self.assertRaises(DataError):
                item.save()

        with transaction.atomic():
            item.description = 'x' * 70
            with self.assertRaises(DataError):
                item.save()

        with transaction.atomic():
            item.udVta = 'x' * 4
            with self.assertRaises(DataError):
                item.save()

        with transaction.atomic():
            item.access_key = 'x' * 20
            with self.assertRaises(DataError):
                item.save()

        with transaction.atomic():
            item.standar_cost = pow(10, 15)
            with self.assertRaises(DataError):
                item.save()

        with transaction.atomic():
            item.standar_cost = pow(.1, 5)
            with self.assertRaises(DataError):
                item.save()

    def test_not_nulls(self):
        item = self.item

        with transaction.atomic():
            item.item_id = None
            with self.assertRaises(IntegrityError):
                item.save()

        with transaction.atomic():
            item.description = None
            with self.assertRaises(IntegrityError):
                item.save()

        with transaction.atomic():
            item.udVta = None
            with self.assertRaises(IntegrityError):
                item.save()

        with transaction.atomic():
            item.access_key = None
            with self.assertRaises(IntegrityError):
                item.save()

        with transaction.atomic():
            item.standar_cost = None
            with self.assertRaises(IntegrityError):
                item.save()

        with transaction.atomic():
            item.standar_cost = None
            with self.assertRaises(IntegrityError):
                item.save()

        with transaction.atomic():
            item.company = None
            with self.assertRaises(IntegrityError):
                item.save()
