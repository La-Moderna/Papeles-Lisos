from decimal import Decimal

from companies.models import Company

from django.urls import reverse

from inventories.models import Item
from inventories.serializers import RetrieveItemSerializer

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ItemsAPITestCase(APITestCase):
    """Test /items endpoint."""
    def setUp(self):
        self.user = User.objects.create(
            email='user@test.com',
            name='Tester',
        )

        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

        self.company_1 = Company.objects.create(
            id='222',
            name="Ejemplo 1"
        )

        self.company_2 = Company.objects.create(
            id='333',
            name="Ejemplo 2"
        )

        self.item_1 = Item.objects.create(
            id="10011262",
            description="L-3",
            udVta="MIL",
            access_key="905",
            standar_cost=0.9631,
            company=self.company_1
        )

        self.item_2 = Item.objects.create(
            id="10015474",
            description="61200005001",
            udVta="MIL",
            access_key="864",
            standar_cost=2.0583,
            company=self.company_1
        )

        self.item_3 = Item.objects.create(
            id="10015814",
            description="61500004001",
            udVta="MIL",
            access_key="864",
            standar_cost=0.979,
            company=self.company_2
        )

        self.item_4 = Item.objects.create(
            id="10015852",
            description="AMMENS 60 G",
            udVta="MIL",
            access_key="876",
            standar_cost=1.912,
            company=self.company_2
        )

        data = {
            "email": self.user.email,
            "password": self.password
        }

        response = self.client.post(
            reverse('auth-list'),
            data
        )

        self.token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_list_items(self):
        '''Test valid list of items'''

        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = Item.objects.all()
        item_serializer = RetrieveItemSerializer(items, many=True)

        self.assertEqual(item_serializer.data, response.data)

    def test_retrieve_item(self):
        '''Test valid retrive item with a valid id'''
        response = self.client.get(
            reverse('item-detail', args=[self.item_1.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item_serializer = RetrieveItemSerializer(self.item_1)

        self.assertEqual(item_serializer.data, response.data)

    def test_create_company(self):
        '''Test valid creation of item'''
        item_data = {
            "id": "10016862",
            "description": "CLM",
            "udVta": "MIL",
            "access_key": "13002",
            "standar_cost": 2.1444,
            "company": self.company_2.id
        }

        response = self.client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        item = Item.objects.get(id=item_data['id'])
        item_serializer = RetrieveItemSerializer(item)

        self.assertEqual(item_serializer.data, response.data)

    def test_partial_update_item_description(self):
        '''Test valid update of item description'''
        item_data = {
            "description": "Update",
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=self.item_1.id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.description, item_data['description'])

    def test_partial_update_item_udVta(self):
        '''Test valid update of item udVta'''
        item_data = {
            "udVta": "KGS",
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=self.item_1.id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.udVta, item_data['udVta'])

    def test_partial_update_item_access_key(self):
        '''Test valid update of item access_key'''
        item_data = {
            "access_key": "Update",
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=self.item_1.id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.access_key, item_data['access_key'])

    def test_partial_update_item_standar_cost(self):
        '''Test valid update of item standar_cost'''
        item_data = {
            "standar_cost": 1.1111,
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=self.item_1.id)

        self.assertDictContainsSubset({
            "standar_cost": "1.1111"
        }, response.data)

        self.assertEqual(
            item.standar_cost,
            Decimal("1.1111")
        )

    def test_partial_update_item_company(self):
        '''Test valid update of item company'''
        item_data = {
            "company": self.company_2.id,
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=self.item_1.id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.company.id, item_data['company'])

    def test_partial_update_item_id(self):
        '''Test valid update of item id'''
        item_data = {
            "id": "30016214",
        }

        old_id = self.item_1.id

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=item_data["id"])

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.id, item_data['id'])

        item_list = Item.objects.filter(id=old_id)

        self.assertEqual(len(item_list), 0)

    def test_destroy_item(self):
        '''Test valid destroy item, updating the is_active value'''
        response = self.client.delete(
            reverse('item-detail',  kwargs={'pk': self.item_1.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(pk=self.item_1.id)
        self.assertEqual(item.is_active, False)

    def test_list_item_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(reverse('item-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_item_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(
            reverse('item-detail', args=[self.item_2.id])
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_item_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        item_data = {
            "id": "10216862",
            "description": "CLM",
            "udVta": "MIL",
            "access_key": "13002",
            "standar_cost": 2.1444,
            "company": self.company_2.id
        }

        response = client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_item_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.delete(
            reverse('item-detail',  kwargs={'pk': self.item_3.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_item_invalid_id(self):
        '''Test no valid request with incorrect id'''

        response = self.client.delete(
            reverse('item-detail',  args=[{'id': '000'}])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_item_none_values(self):
        '''Test no valid create request with missing fields'''
        item_data = {}

        response = self.client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "id": [
                    "This field is required."
                ],
                "description": [
                    "This field is required."
                ],
                "udVta": [
                    "This field is required."
                ],
                "access_key": [
                    "This field is required."
                ],
                "standar_cost": [
                    "This field is required."
                ],
                "company": [
                    "This field is required."
                ]
            },
            response.data
        )

    def test_create_item_blank_fields(self):
        '''Test no valid create request with blank fields'''
        item_data = {
            "id": "",
            "description": "",
            "udVta": "",
            "access_key": "",
            "standar_cost": "",
            "company": ""
        }

        response = self.client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "id": [
                    "This field may not be blank."
                ],
                "description": [
                    "This field may not be blank."
                ],
                "udVta": [
                    "This field may not be blank."
                ],
                "access_key": [
                    "This field may not be blank."
                ],
                "standar_cost": [
                    "A valid number is required."
                ],
                "company": [
                    "This field may not be null."
                ]
            },
            response.data
        )

    def test_create_item_invalid_company(self):
        '''Test no valid create request with a non-existent company'''
        item_data = {
            "id": "13215474",
            "description": "61200005001",
            "udVta": "MIL",
            "access_key": "864",
            "standar_cost": 2.0583,
            "company": "000"
        }

        response = self.client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "company": [
                    'Invalid pk "000" - object does not exist.'
                ]
            },
            response.data
        )

    def test_create_item_invalid_id(self):
        '''Test no valid create request with an existing id'''
        item_data = {
            "id": self.item_4.id,
            "description": "61200005001",
            "udVta": "MIL",
            "access_key": "864",
            "standar_cost": 2.0583,
            "company": "222"
        }

        response = self.client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "id": [
                    'item with this id already exists.'
                ]
            },
            response.data
        )
