from decimal import Decimal

from companies.models import Company

from django.urls import reverse

from inventories.models import Inventory, Item, Warehouse
from inventories.serializers import RetrieveItemSerializer

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class InventoryAPITestCase(APITestCase):
    """ Basic tests"""
    def setUp(self):
        self.url_auth = reverse('auth-list')
        self.usuario = User.objects.create_user("prueba3@gmail.com",
                                                "root")

        self.company_1 = Company.objects.create(
            company_id='222',
            name="Ejemplo 1"
        )
        self.warehouse_dummy = Warehouse.objects.create(
            name="12c",
            description='for testing in another way',
            company=self.company_1)
        self.warehouse_dummy_3 = Warehouse.objects.create(
            name="43a",
            description='for testing updates',
            company=self.company_1)
        self.item_1 = Item.objects.create(
            item_id="10011262",
            description="L-3",
            udVta="MIL",
            access_key="905",
            standar_cost=0.9631,
            company=self.company_1
        )
        self.get_inventory_list_url = reverse('inventories-list')
        self.create_inventory_url = reverse('inventories-list')
        self.get_warehouse_list_url = reverse('warehouses-list')
        self.inventory_data = {
            'stock': 3000.00,
            'warehouse': self.warehouse_dummy.id,
            'item': self.item_1.id
        }
        self.warehouse_data = {
            'description': 'This is for testing'
        }
        self.correct_whs_data_update = {
            'status': False
        }
        self.usuario_dummy = User.objects.get(email="prueba3@gmail.com")
        self.user_data = {
            "email": self.usuario_dummy.email,
            "password": "root"
        }

    def api_authentication(self):
        res = self.client.post(self.url_auth, self.user_data)

        token = res.json()['token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

    def test_create_inventory_fails_no_data_no_token(self):

        res = self.client.post(self.create_inventory_url)

        self.assertEqual(res.status_code, 401)

    def test_create_inventory_fails_without_data_with_token(self):
        """Test fails to create inventory with no data"""

        self.api_authentication()

        res = self.client.post(self.create_inventory_url)

        self.assertEqual(res.status_code, 400)

        self.assertDictContainsSubset(
            {
                "warehouse": [
                    "This field is required."
                ]
            },
            res.data
        )

    def test_list_inventories(self):
        """Test valid list of inventories"""

        self.api_authentication()

        res = self.client.get(
            self.get_inventory_list_url)

        self.assertEqual(res.status_code, 200)

    def test_create_inventory_fails_with_data_no_token(self):
        """Test fails create inventory without token"""

        res = self.client.post(
            self.create_inventory_url,
            self.inventory_data)

        self.assertEqual(res.status_code, 401)

    def test_create_inventory_succesfully_with_data_success_token(self):
        """Test create succesfully inventory"""

        self.api_authentication()

        res = self.client.post(self.create_inventory_url,
                               self.inventory_data)

        self.assertEqual(res.status_code, 201)

    def test_retrieve_one_existing_inventory(self):
        """Test retrieve one inventory"""
        self.api_authentication()

        self.company_2 = Company.objects.create(
            company_id='225',
            name="Ejemplo 2"
        )
        self.warehouse_dummy_2 = Warehouse.objects.create(
            name="tes5",
            description='testing 1 object retrieval',
            company=self.company_2)

        self.inventory_dummy = Inventory.objects.create(
            stock=3500.51,
            warehouse=self.warehouse_dummy_2,
            item=self.item_1)

        res = self.client.get(
            self.get_inventory_list_url+"/"+str(self.inventory_dummy.id))

        self.assertEqual(res.status_code, 200)

        self.assertDictContainsSubset(
            {
                'stock': str(self.inventory_dummy.stock),
            }, res.data)

    def test_retrieve_non_existing_inventory_fails_no_token(self):
        """Test fails to retrieve non existing inventory"""

        res = self.client.get(
            self.get_inventory_list_url+'/'+str(50)
            )

        self.assertEqual(res.status_code, 401)

    def test_retrieve_non_existing_inventory_success_token_fails(self):
        """Test fails retrieve non existing inventory with token"""

        self.api_authentication()
        print("Probando chistosas: ", self.get_warehouse_list_url+'/'+str(50))
        res = self.client.get(
            self.get_warehouse_list_url+'/'+str(50))

        self.assertEqual(res.status_code, 404)

    def test_create_inventory_with_enourmus_number_type_no_token_fails(self):
        """Test to create an inventory with wrong data type fails"""

        self.dummy_inventory_data = {
            'stock': 10000000*1000000,
            'warehouse': self.warehouse_dummy.id,
            'item': self.item_1.id
        }

        res = self.client.post(
            self.create_inventory_url,
            self.dummy_inventory_data
        )

        self.assertEqual(res.status_code, 401)

    def test_create_inventory_with_big_number_and_sc_token_fails(self):
        """Test to create inventory with not accepted data type fails"""

        self.api_authentication()

        self.dummy_inventory_data = {
            'stock': 10000000*1000000,
            'warehouse': self.warehouse_dummy.id,
            'item': self.item_1.id
        }

        res = self.client.post(
            self.create_inventory_url,
            self.dummy_inventory_data)

        self.assertEqual(res.status_code, 400)

    def test_create_inventory_with_wrong_type_no_token_fails(self):
        """Test to create an inventory with wrong stock data type fails"""

        self.wrong_inventory_data = {
            'stock': 'test_string',
            'warehouse': self.warehouse_dummy.id,
            'item': self.item_1.id
        }

        res = self.client.post(
            self.create_inventory_url,
            self.wrong_inventory_data
        )

        self.assertEqual(res.status_code, 401)

    def test_create_inventory_with_wrong_type_succ_token_fails(self):
        """Test to create inventory wrong stock data, success token fails"""

        self.api_authentication()

        self.wrong_inventory_data = {
            'stock': 'test_string',
            'warehouse': self.warehouse_dummy.id,
            'item': self.item_1.id
        }

        res = self.client.post(
            self.create_inventory_url,
            self.wrong_inventory_data)

        self.assertEqual(res.status_code, 400)

    def test_create_inventory_not_foreign_key_no_token_fails(self):
        """Test create inventory with non existing FK no token fails"""

        self.false_inventory_data = {
            'stock': 3000.00,
        }
        res = self.client.post(
            self.create_inventory_url,
            self.false_inventory_data
        )
        self.assertEqual(res.status_code, 401)

    def test_create_inventory_not_foreign_key_success_token_fails(self):
        """Test create inventory with a non existing foreign key fails"""

        self.api_authentication()

        self.false_inventory_data = {
            'stock': 3000.00,
        }

        res = self.client.post(
            self.create_inventory_url,
            self.false_inventory_data)

        self.assertEqual(res.status_code, 400)

    def test_create_inventory_false_foreign_key_success_token_fails(self):
        """Test create inventory with false foreign key fails"""

        self.api_authentication()

        self.false_w_inventory_data = {
            'stock': 3000.00,
            'warehouse': 20,
            'item': self.item_1.id
        }

        res = self.client.post(
            self.create_inventory_url,
            self.false_w_inventory_data)

        self.assertEqual(res.status_code, 400)

    def test_update_inventory_stock(self):
        """Test valid updates stock of inventory"""
        self.api_authentication()
        self.inventory_dummy_3 = Inventory.objects.create(
            stock=3500.51,
            warehouse=self.warehouse_dummy,
            item=self.item_1)
        inventory_data = {
            "stock": 4790
        }

        res = self.client.patch(
            reverse('inventories-detail',
                    kwargs={'pk': self.inventory_dummy_3.id}),
            inventory_data)

        self.assertEqual(res.status_code, 200)

    def test_update_inventory_related_company(self):
        """Test valid to update fk related to an inventory """
        self.api_authentication()
        inventory_dummy_3 = Inventory.objects.create(
            stock=3500.51,
            warehouse=self.warehouse_dummy,
            item=self.item_1)
        inventory_data = {
            "warehouse": self.warehouse_dummy_3.id
        }

        res = self.client.patch(
            reverse('inventories-detail',
                    kwargs={'pk': inventory_dummy_3.id}),
            inventory_data)

        self.assertEqual(res.status_code, 200)

    def test_destroy_inventory(self):
        """Test valid destroy inventory, updates is_active to false"""

        inventory_dummy_4 = Inventory.objects.create(
            stock=3600.51,
            warehouse=self.warehouse_dummy,
            item=self.item_1)

        self.api_authentication()
        res = self.client.delete(
            reverse('inventories-detail', kwargs={'pk': inventory_dummy_4.id})
        )
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        self.usuario.delete()
        self.warehouse_dummy.delete()
        self.usuario_dummy.delete()


class WarehouseAPITestCase(APITestCase):
    def setUp(self):

        self.url_auth = reverse('auth-list')

        self.usuario = User.objects.create_user("prueba3@gmail.com",
                                                "root")
        self.company_1 = Company.objects.create(
            company_id='222',
            name="Ejemplo 1"
        )
        self.warehouse_dummy = Warehouse.objects.create(
            name="456v",
            description='for testing in another way',
            company=self.company_1)

        self.create_warehouse_url = reverse('warehouses-list')

        self.get_warehouse_list_url = reverse('warehouses-list')

        self.warehouse_data = {
            'id': '2',
            'name': '34g',
            'description': 'This is for testing',
            'company': self.company_1.id
        }

        self.correct_whs_data_update = {
            'status': False
        }

        self.usuario_dummy = User.objects.get(email="prueba3@gmail.com")

        self.user_data = {
            "email": self.usuario_dummy.email,
            "password": "root"
        }

    def api_authentication(self):

        res = self.client.post(self.url_auth, self.user_data)

        token = res.json()['token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

    def test_create_warehouse_without_data_no_token_fails(self):
        """Test create warehouse with no data no token fails"""

        res = self.client.post(self.create_warehouse_url)

        self.assertEqual(res.status_code, 401)

    def test_create_warehouse_without_data_with_token_fails(self):
        """Test create warehouse without data fails"""

        self.api_authentication()

        res = self.client.post(self.create_warehouse_url)

        self.assertEqual(res.status_code, 400)

        self.assertDictContainsSubset(
            {
                "description": [
                    "This field is required."
                ],
            },
            res.data

        )

    def test_create_warehouse_with_data_no_token_fails(self):
        """Test create warehouse without token fails"""

        res = self.client.post(self.create_warehouse_url,
                               self.warehouse_data)
        self.assertEqual(res.status_code, 401)

    def test_create_warehouse_with_data_token_success(self):
        """Test correct creation of warehouse"""

        self.api_authentication()

        res = self.client.post(self.create_warehouse_url,
                               self.warehouse_data)

        self.assertEqual(res.status_code, 201)

    def test_list_warehouses_no_token_fails(self):
        """Test to retrieve warehouses withouth token fails"""

        res = self.client.get(self.get_warehouse_list_url)

        self.assertEqual(res.status_code, 401)

    def test_list_warehouses_success_token(self):
        """Test lists correctly warehouses"""

        self.api_authentication()

        res = self.client.get(self.get_warehouse_list_url)

        self.assertEqual(res.status_code, 200)

    def test_retrieve_existing_warehouse_no_token_fails(self):
        """Test retrieve warehouse without token fails"""

        self.warehouse_dummy_2 = Warehouse.objects.create(
            name="34c",
            description='testing 1 object retrieval',
            company=self.company_1)

        res = self.client.get(
            self.get_warehouse_list_url+'/'+str(self.warehouse_dummy.id)
        )

        self.assertEqual(res.status_code, 401)

    def test_retrieve_existing_warehouse_success_token(self):
        """Test retrieve warehouse correctly"""
        self.api_authentication()

        self.warehouse_dummy_2 = Warehouse.objects.create(
            name="32c",
            description='testing 1 object retrieval',
            company=self.company_1)

        res = self.client.get(
            self.get_warehouse_list_url+'/'+str(self.warehouse_dummy_2.id))

        self.assertEqual(res.status_code, 200)

        self.assertDictContainsSubset(
            {
                'id': self.warehouse_dummy_2.id,
                'description': self.warehouse_dummy_2.description,
                'company': self.company_1.id
            }, res.data)

    def test_retrieve_non_existing_warehouse_no_token_fails(self):
        """Test to retrieve non existing warehouse no token fails"""

        res = self.client.get(
            self.get_warehouse_list_url+'/'+str(50)
            )

        self.assertEqual(res.status_code, 401)

    def test_retrieve_non_existing_warehouse_success_token_fails(self):
        """Test retrieve non existing warehouse with token fails"""

        self.api_authentication()

        res = self.client.get(
            self.get_warehouse_list_url+'/'+str(50))

        self.assertEqual(res.status_code, 404)

    def test_create_warehouse_with_larger_data_no_token_fails(self):
        """Test create a warehouse with wrong data type fails"""

        self.dummy_warehouse_data = {
            'id': '2',
            'name': '45t',
            'description': 'x'*255
            }

        res = self.client.post(
            self.create_warehouse_url,
            self.dummy_warehouse_data
        )

        self.assertEqual(res.status_code, 401)

    def test_create_warehouse_with_larger_data_succ_token_fails(self):
        """Test create warehouse with larger description fails"""

        self.api_authentication()

        self.dummy_warehouse_data = {
            'name': '34t',
            'id': '2',
            'description': 'x'*255
            }

        res = self.client.post(
            self.create_warehouse_url,
            self.dummy_warehouse_data)

        self.assertEqual(res.status_code, 400)

    def test_update_warehouse_description(self):
        """Test to update warehouse description"""

        self.api_authentication()
        warehouse_dummy_6 = Warehouse.objects.create(
            name="tes2",
            description="This is for testing",
            company=self.company_1
        )
        warehouse_data = {
            "description": "This is the updated description"
        }

        res = self.client.patch(
            reverse('warehouses-detail',
                    kwargs={'pk': warehouse_dummy_6.id}),
            warehouse_data)
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        self.usuario.delete()
        self.warehouse_dummy.delete()
        self.usuario_dummy.delete()


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
            company_id='222',
            name="Ejemplo 1"
        )

        self.company_2 = Company.objects.create(
            company_id='333',
            name="Ejemplo 2"
        )

        self.item_1 = Item.objects.create(
            item_id="10011262",
            description="L-3",
            udVta="MIL",
            access_key="905",
            standar_cost=0.9631,
            company=self.company_1
        )

        self.item_2 = Item.objects.create(
            item_id="10015474",
            description="61200005001",
            udVta="MIL",
            access_key="864",
            standar_cost=2.0583,
            company=self.company_1
        )

        self.item_3 = Item.objects.create(
            item_id="10015814",
            description="61500004001",
            udVta="MIL",
            access_key="864",
            standar_cost=0.979,
            company=self.company_2
        )

        self.item_4 = Item.objects.create(
            item_id="10015852",
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
            reverse('item-detail', args=[self.item_1.item_id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item_serializer = RetrieveItemSerializer(self.item_1)

        self.assertEqual(item_serializer.data, response.data)

    def test_create_company(self):
        '''Test valid creation of item'''
        item_data = {
            "item_id": "10016862",
            "description": "CLM",
            "udVta": "MIL",
            "access_key": "13002",
            "standar_cost": 2.1444,
            "company": self.company_2.company_id
        }

        response = self.client.post(reverse('item-list'), item_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        item = Item.objects.get(item_id=item_data['item_id'])
        item_serializer = RetrieveItemSerializer(item)

        self.assertEqual(item_serializer.data, response.data)

    def test_partial_update_item_description(self):
        '''Test valid update of item description'''
        item_data = {
            "description": "Update",
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.item_id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=self.item_1.item_id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.description, item_data['description'])

    def test_partial_update_item_udVta(self):
        '''Test valid update of item udVta'''
        item_data = {
            "udVta": "KGS",
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.item_id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=self.item_1.item_id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.udVta, item_data['udVta'])

    def test_partial_update_item_access_key(self):
        '''Test valid update of item access_key'''
        item_data = {
            "access_key": "Update",
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.item_id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=self.item_1.item_id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.access_key, item_data['access_key'])

    def test_partial_update_item_standar_cost(self):
        '''Test valid update of item standar_cost'''
        item_data = {
            "standar_cost": 1.1111,
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.item_id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=self.item_1.item_id)

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
            "company": self.company_2.company_id,
        }

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.item_id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=self.item_1.item_id)

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.company.company_id, item_data['company'])

    def test_partial_update_item_id(self):
        '''Test valid update of item id'''
        item_data = {
            "item_id": "30016214",
        }

        old_id = self.item_1.item_id

        response = self.client.patch(
            reverse('item-detail', kwargs={'pk': self.item_1.item_id}),
            item_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=item_data["item_id"])

        self.assertDictContainsSubset(item_data, response.data)

        self.assertEqual(item.item_id, item_data['item_id'])

        item_list = Item.objects.filter(item_id=old_id)

        self.assertEqual(len(item_list), 0)

    def test_destroy_item(self):
        '''Test valid destroy item, updating the is_active value'''
        response = self.client.delete(
            reverse('item-detail',  kwargs={'pk': self.item_1.item_id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(item_id=self.item_1.item_id)
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
                "item_id": [
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
                "item_id": [
                    "This field is required."
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
            "item_id": "13215474",
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
                    'Object with company_id=000 does not exist.'
                ]
            },
            response.data
        )

    def test_create_item_invalid_id(self):
        '''Test no valid create request with an existing id'''
        item_data = {
            "item_id": self.item_4.item_id,
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
                "item_id": [
                    'item with this item id already exists.'
                ]
            },
            response.data
        )
