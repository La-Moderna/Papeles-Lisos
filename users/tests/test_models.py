""" Tests for users of the application."""
from unittest import mock

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from django.utils import timezone

from users.models import Permission, Role, User


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

    def test_not_nulls(self):
        """Test not_null fields."""
        user = self.user

        with transaction.atomic():
            user.email = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.name = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.last_name = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.last_name = None
            with self.assertRaises(IntegrityError):
                user.save()

        with transaction.atomic():
            user.password = None
            with self.assertRaises(IntegrityError):
                user.save()

    def test_nulls(self):
        """Test null fields."""
        user = self.user

        user.last_login = None
        user.save()
        self.assertEqual(user.last_login, None)

        user.created_date = None
        user.save()
        self.assertEqual(user.created_date, None)

    def test_string_representation(self):
        """Test __str__ and get_short_name methods"""
        user = self.user
        self.assertEqual(str(user), user.email)
        self.assertEqual(user.get_short_name(), user.email)

    def test_created_date(self):
        """Test created_date field"""
        user = self.user
        self.assertEqual(timezone.now().date(), user.created_date.date())
        self.assertEqual(timezone.now().date(), user.last_modified.date())

    def test_auto_now(self):
        """Test auto now fields."""
        user = self.user
        mocked = timezone.localtime()
        with mock.patch('django.utils.timezone.now', mock.Mock(
            return_value=mocked
        )):
            user.name = "Test last_modified"
            user.save()
            self.assertEqual(user.last_modified, mocked)

    def test_defaults(self):
        """Test default values."""
        user = self.user
        self.assertEqual(user.last_name, 'none')
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_active, True)


class RoleTestCase(TestCase):
    "Test Role model."
    def setUp(self):
        self.role = Role.objects.create(
            name="TEST"
        )

    def test_max_length(self):
        """Test max_length values."""
        role = self.role
        with transaction.atomic():
            role.name = 'x'*255
            with self.assertRaises(DataError):
                role.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        role = self.role

        with transaction.atomic():
            role.name = None
            with self.assertRaises(IntegrityError):
                role.save()


class PermissionTestCase(TestCase):
    "Test Permission model."
    def setUp(self):
        self.permission = Permission.objects.create(
            codename="TEST",
            description="This is a test"
        )

    def test_max_length(self):
        """Test max_length values."""
        permission = self.permission
        with transaction.atomic():
            permission.codename = 'x'*255
            with self.assertRaises(DataError):
                permission.save()

        with transaction.atomic():
            permission.description = 'x'*255
            with self.assertRaises(DataError):
                permission.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        permission = self.permission

        with transaction.atomic():
            permission.codename = None
            with self.assertRaises(IntegrityError):
                permission.save()

        with transaction.atomic():
            permission.description = None
            with self.assertRaises(IntegrityError):
                permission.save()
