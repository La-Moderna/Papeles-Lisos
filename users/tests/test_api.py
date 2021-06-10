import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Permission, Role, User


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
            {'id', 'email', 'roles'},
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


class RoleAPITestCase(APITestCase):
    """Test roles endpoint"""
    def setUp(self):
        self.url_auth = reverse('auth-list')
        self.user = User.objects.create_user("test@gmail.com",
                                             "root")
        self.user_info = {
            'email': self.user.email,
            "password": "root"
        }
        self.permission_1 = Permission.objects.create(codename="test_add",
                                                      description="is test")
        self.permission_2 = Permission.objects.create(codename="add_test",
                                                      description="test 2")

        self.role_1 = Role.objects.create(name="gti")
        self.role_data = {
            "name": "TEST",
            "permissions": [
                self.permission_1.id
                ]
        }
        self.role_data_1 = {
            "name": "TST1",
            "permissions": [
                self.permission_1.id,
                self.permission_2.id
                ]
        }

        self.get_roles_list_url = reverse('role-list')
        self.create_role_url = reverse('role-list')
        self.get_permissions_list_url = reverse('permission-list')

    def api_authentication(self):
        res = self.client.post(self.url_auth,
                               self.user_info)

        token = res.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

    def test_create_role_fails_without_token_nor_data(self):

        res = self.client.post(self.create_role_url)
        self.assertEqual(res.status_code, 401)

    def test_create_role_fails_without_token(self):
        """Test fails to create role without fields"""

        self.api_authentication()
        res = self.client.post(self.create_role_url)
        self.assertEqual(res.status_code, 400)

    def test_create_role_fails_with_info_not_token(self):
        """Test fails to create role without token"""

        res = self.client.post(self.create_role_url,
                               self.role_data)
        self.assertEqual(res.status_code, 401)

    def test_create_role_success_with_correct_info(self):
        """Test creates role with necessary fields"""

        self.api_authentication()
        res = self.client.post(self.create_role_url,
                               self.role_data)
        self.assertEqual(res.status_code, 201)

    def test_list_roles_fails_without_token(self):
        """Test fails to list roles without token"""

        res = self.client.get(self.get_roles_list_url)
        self.assertEquals(res.status_code, 401)

    def test_list_roles_with_token_success(self):
        """Test list roles successfully"""

        self.api_authentication()

        res = self.client.get(self.get_roles_list_url)
        self.assertEquals(res.status_code, 200)

    def test_retrieve_role_fails_without_token_nor_pk(self):
        """Test retrieve role fails without token nor pk"""

        res = self.client.get(self.get_roles_list_url+'/'+'45')
        self.assertEquals(res.status_code, 401)

    def test_retrieve_fails_non_existing_pk(self):
        """Test fails to retrieve non existing role"""

        self.api_authentication()
        res = self.client.get(self.get_roles_list_url+'/'+'45')
        self.assertEquals(res.status_code, 404)

    def test_retrieve_role_successfully_with_token(self):
        """Test retrieves role successfully"""

        self.api_authentication()
        res = self.client.get(self.get_roles_list_url+'/' +
                              str(self.role_1.id))
        self.assertEquals(res.status_code, 200)

    def test_create_role_with_permissions_fails_no_token(self):
        """Test to create role with permissions fails without token"""

        res = self.client.post(self.create_role_url,
                               self.role_data)
        self.assertEquals(res.status_code, 401)

    def test_create_role_with_permissions_successfully(self):
        """test to successfully create role with permissions"""

        self.api_authentication()
        res = self.client.post(self.create_role_url,
                               self.role_data_1)
        self.assertEquals(res.status_code, 201)

    def test_destroys_role_fails_without_token(self):
        """Test fails to destroy role without token"""

        res = self.client.delete(self.create_role_url)
        self.assertEquals(res.status_code, 401)

    def test_destroys_role_successfully(self):
        """Test to destroy(logically) a role"""

        self.api_authentication()
        res = self.client.delete(self.create_role_url+'/'+str(self.role_1.id))
        self.assertEquals(res.status_code, 200)

    def tearDown(self):
        return super().tearDown()


class RoleUserAPITestCase(APITestCase):
    """Test add roles to user"""

    def setUp(self):
        self.url_auth = reverse('auth-list')
        self.user = User.objects.create_user("test2@gmail.com",
                                             "root")
        self.user_info = {
            'email': self.user.email,
            "password": "root"
        }

        self.role_1 = Role.objects.create(name="VTEST")
        self.role_2 = Role.objects.create(name="TES2")
        self.role_3 = Role.objects.create(name="VYUT")

        self.roles_array = [
                self.role_1.id,
                self.role_2.id,
                self.role_3.id
            ]

        self.roles_data = {
            'roles': [
               self.role_1.id,
               self.role_2.id,
               self.role_3.id
            ]
        }
        self.roles_data_dummy = {
            'roles': [
                34
            ]
        }

        self.get_roles_list_url = reverse('role-list')
        self.get_permissions_list_url = reverse('permission-list')

    def api_authentication(self):
        res = self.client.post(self.url_auth,
                               self.user_info)
        token = res.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

    def test_add_role_user_fails_without_token(self):
        """Test to add role to user fails with no token"""

        res = self.client.patch(reverse('user_role_add-detail',
                                kwargs={'pk': self.user.id}),
                                json.dumps(self.roles_data),
                                content_type='application/json')

        self.assertEquals(res.status_code, 401)

    def test_add_role_to_non_existent_user_fails(self):
        """Test fails to add roles to a non existing user"""

        self.api_authentication()
        res = self.client.patch(reverse('user_role_add-detail',
                                kwargs={'pk': 78}),
                                json.dumps(self.roles_data),
                                content_type='application/json')

        self.assertEquals(res.status_code, 404)

    def test_add_non_existing_role_fails(self):
        """Test fails to add a non existing role"""
        self.api_authentication()
        res = self.client.patch(reverse('user_role_add-detail',
                                kwargs={'pk': self.user.id}),
                                json.dumps(self.roles_data_dummy),
                                content_type='application/json')

        self.assertEquals(res.status_code, 400)

    def test_add_role_user_successfully(self):
        """Test succeeds to add roles to an existing user"""

        self.api_authentication()
        res = self.client.patch(reverse('user_role_add-detail',
                                kwargs={'pk': self.user.id}),
                                json.dumps(self.roles_data),
                                content_type='application/json')

        self.assertEquals(res.status_code, 200)
