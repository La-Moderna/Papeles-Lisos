from companies.models import Company

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from inventories.models import Item


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
