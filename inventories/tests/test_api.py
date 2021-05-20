import random

from companies.models import Company

from django.urls import reverse

from inventories.models import Inventory, Warehouse

from rest_framework.test import APITestCase

from users.models import User


class InventoryAPITestCase(APITestCase):

    ############################################
    # Hacer tests de update de parametros
    # Hacer tests de delete de parametros
    ############################################

    """ Basic tests"""
    def setUp(self):
        self.url_auth = reverse('auth-list')
        self.usuario = User.objects.create_user("prueba3@gmail.com",
                                                "root")
        self.company_1 = Company.objects.create(
            id='222',
            name="Ejemplo 1"
        )
        self.warehouse_dummy = Warehouse.objects.create(
            warehouse_name="12c",
            description='for testing in another way',
            company=self.company_1)
        self.warehouse_dummy_3 = Warehouse.objects.create(
            warehouse_name="43a",
            description='for testing updates',
            company=self.company_1)
        self.get_inventory_list_url = reverse('inventories-list')
        self.create_inventory_url = reverse('inventories-list')
        self.get_warehouse_list_url = reverse('warehouses-list')
        self.inventory_data = {
            'stock': 3000.00,
            'warehouse': self.warehouse_dummy.id
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
            id='225',
            name="Ejemplo 2"
        )
        self.warehouse_dummy_2 = Warehouse.objects.create(
            warehouse_name="tes5",
            description='testing 1 object retrieval',
            company=self.company_2)

        self.inventory_dummy = Inventory.objects.create(
            stock=3500.51,
            warehouse=self.warehouse_dummy_2)

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
            self.get_inventory_list_url+str(random.randint(1, 10)*5536)
            )

        self.assertEqual(res.status_code, 404)

    def test_retrieve_non_existing_inventory_success_token_fails(self):
        """Test fails retrieve non existing inventory with token"""

        self.api_authentication()

        res = self.client.get(
            self.get_warehouse_list_url+str(random.randint(1, 10)*5536))

        self.assertEqual(res.status_code, 404)

    def test_create_inventory_with_enourmus_number_type_no_token_fails(self):
        """Test to create an inventory with wrong data type fails"""

        self.dummy_inventory_data = {
            'stock': 10000000*1000000,
            'warehouse': self.warehouse_dummy.id
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
            'warehouse': self.warehouse_dummy.id
        }

        res = self.client.post(
            self.create_inventory_url,
            self.dummy_inventory_data)

        self.assertEqual(res.status_code, 400)

    def test_create_inventory_with_wrong_type_no_token_fails(self):
        """Test to create an inventory with wrong stock data type fails"""

        self.wrong_inventory_data = {
            'stock': 'test_string',
            'warehouse': self.warehouse_dummy.id
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
            'warehouse': self.warehouse_dummy.id
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
            'warehouse': 20
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
            warehouse=self.warehouse_dummy)
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
            warehouse=self.warehouse_dummy)
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
            warehouse=self.warehouse_dummy)

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
            id='222',
            name="Ejemplo 1"
        )
        self.warehouse_dummy = Warehouse.objects.create(
            warehouse_name="456v",
            description='for testing in another way',
            company=self.company_1)

        self.create_warehouse_url = reverse('warehouses-list')

        self.get_warehouse_list_url = reverse('warehouses-list')

        self.warehouse_data = {
            'id': '2',
            'warehouse_name': '34g',
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
                "company": [
                    "This field is required."
                ]
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
            warehouse_name="34c",
            description='testing 1 object retrieval',
            company=self.company_1)

        res = self.client.get(
            self.get_warehouse_list_url+"/"+str(self.warehouse_dummy.id)
        )

        self.assertEqual(res.status_code, 401)

    def test_retrieve_existing_warehouse_success_token(self):
        """Test retrieve warehouse correctly"""
        self.api_authentication()

        self.warehouse_dummy_2 = Warehouse.objects.create(
            warehouse_name="32c",
            description='testing 1 object retrieval',
            company=self.company_1)

        res = self.client.get(
            self.get_warehouse_list_url+"/"+str(self.warehouse_dummy_2.id))

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
            self.get_warehouse_list_url+"/"+str(random.randint(1, 10)*5356)
            )

        self.assertEqual(res.status_code, 401)

    def test_retrieve_non_existing_warehouse_success_token_fails(self):
        """Test retrieve non existing warehouse with token fails"""

        self.api_authentication()

        res = self.client.get(
            self.get_warehouse_list_url+"/"+str(random.randint(1, 10)*535))

        self.assertEqual(res.status_code, 404)

    def test_create_warehouse_with_larger_data_no_token_fails(self):
        """Test create a warehouse with wrong data type fails"""

        self.dummy_warehouse_data = {
            'id': '2',
            'warehouse_name': '45t',
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
            'warehouse_name': '34t',
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
            warehouse_name="tes2",
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


# Checar ultimo test -- el de inventories
