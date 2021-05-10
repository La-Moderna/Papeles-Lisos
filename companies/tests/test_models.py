from django.db import transaction
from django.test import TestCase
from django.db.utils import DataError, IntegrityError

from companies.models import Company


class CompanyTestModels(TestCase):
    """Test Company Model"""

    def setUp(self):
        self.company = Company.objects.create(
            company=1,
            name="PELICULAS PLASTICAS SA DE CV"
        )

    def test_max_length(self):
        company = self.company

        with transaction.atomic():
            company.name = 'x' * 101
            with self.assertRaises(DataError):
                company.save()

    def test_not_nulls(self):
        company = self.company

        with transaction.atomic():
            company.name = None
            with self.assertRaises(IntegrityError):
                company.save()

        with transaction.atomic():
            company.isActive = None
            with self.assertRaises(IntegrityError):
                company.save()

    def test_defaults(self):
        company = self.company

        self.assertEqual(company.is_active, True)
