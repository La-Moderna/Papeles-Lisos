from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from orders.models import Authorization


class AuthorizationTestCase(TestCase):
    """Test Authorization Model"""
    def setUp(self):
        """Init model"""
        self.authorization = Authorization.objects.create()

    def test_not_nulls(self):
        """Test not_null fields."""
        authorization = self.authorization

        with transaction.atomic():
            authorization.vta = None
            with self.assertRaises(IntegrityError):
                authorization.save()

        with transaction.atomic():
            authorization.cst = None
            with self.assertRaises(IntegrityError):
                authorization.save()

        with transaction.atomic():
            authorization.suaje = None
            with self.assertRaises(IntegrityError):
                authorization.save()

        with transaction.atomic():
            authorization.grabado = None
            with self.assertRaises(IntegrityError):
                authorization.save()

        with transaction.atomic():
            authorization.pln = None
            with self.assertRaises(IntegrityError):
                authorization.save()

        with transaction.atomic():
            authorization.ing = None
            with self.assertRaises(IntegrityError):
                authorization.save()

        with transaction.atomic():
            authorization.cxc = None
            with self.assertRaises(IntegrityError):
                authorization.save()

    def test_default(self):
        authotization = self.authorization

        self.assertEqual(authotization.vta, False)
        self.assertEqual(authotization.cst, False)
        self.assertEqual(authotization.suaje, False)
        self.assertEqual(authotization.grabado, False)
        self.assertEqual(authotization.pln, False)
        self.assertEqual(authotization.ing, False)
        self.assertEqual(authotization.cxc, False)
