from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthAPITestCase(APITestCase):
    """Test /auth endpoint."""
    def setUp(self):
        self.user = User.objects.create(
            email='user@test.com',
            name='Tester',
        )
        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

        self.url = reverse('auth-list')

    def test_valid(self):
        """Test valid authentication using self.user credentials."""
        data = {
            "email": self.user.email,
            "password": self.password
        }
        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertDictContainsSubset(
            {"email": self.user.email},
            response.data
        )
        self.assertEqual(
            {'email', 'token'},
            set(response.data.keys())
        )

    def test_missing_fields(self):
        """Test missing fields errors."""
        data = {}
        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertDictContainsSubset(
            {
                "email": [
                    "This field is required."
                ],
                "password": [
                    "This field is required."
                ]
            },
            response.data
        )

    def test_invalid(self):
        """Test invalid credentials."""
        data = {
            "email": self.user.email.replace('@', '1@'),
            "password": self.password
        }
        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertDictContainsSubset(
            {
                "non_field_errors": [
                    "credentials are not valid"
                ]
            },
            response.data
        )

        data = {
            "email": self.user.email,
            "password": self.password+'1'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertDictContainsSubset(
            {
                "non_field_errors": [
                    "credentials are not valid"
                ]
            },
            response.data
        )

    def test_not_activated(self):
        "Test user who is not activated."
        self.user.is_active = False
        self.user.save()
        data = {
            "email": self.user.email,
            "password": self.password
        }
        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertDictContainsSubset(
            {
                "non_field_errors": [
                    "The user has not been activated"
                ]
            },
            response.data
        )

    def tearDown(self):
        return super().tearDown()


class MeAPITestCase(APITestCase):
    """Test /me endpoint."""
    def setUp(self):
        self.user = User.objects.create(
            email='user@test.com',
            name='Tester',
        )
        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

        data = {
            "email": self.user.email,
            "password": self.password
        }
        response = self.client.post(reverse('auth-list'), data)

        if 'token' in response.data.keys():
            self.token = response.data['token']

        self.url = reverse('me-detail')

    def test_valid(self):
        """Test valid call using self.user token from /auth."""
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        response = client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertDictContainsSubset(
            {"email": self.user.email},
            response.data
        )
        self.assertEqual(
            {'id', 'email', 'user_permissions', 'groups'},
            set(response.data.keys())
        )

    def test_invalid(self):
        """Test invalid call using incorrect token."""
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Bearer abc'
        )
        response = client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertDictContainsSubset(
            {"detail": "Invalid signature."},
            response.data
        )

    def test_missing_header(self):
        """Test missing Authorization header."""
        client = self.client
        response = client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertDictContainsSubset(
            {"detail": "Authentication credentials were not provided."},
            response.data
        )

    def tearDown(self):
        return super().tearDown()
