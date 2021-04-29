from django.urls import reverse

from inventories.models import Warehouse

from rest_framework.test import APITestCase


class TestSetUp(APITestCase):

    def setUp(self):

        warehouse_dummy = Warehouse(description='for testing in another way')
        warehouse_dummy.save()
        self.get_inventory_list_url = reverse('inventories-list')
        self.create_inventory_url = reverse('inventories-list')
        self.create_warehouse_url = reverse('warehouses-list')
        self.get_warehouse_list_url = reverse('warehouses-list')
        # self.update_inventory_url = reverse('inventories-detail')
        # self.update_warehouse_url = reverse('warehouses-detail')
        self.inventory_data = {
            'stock': 3000.00,
            'warehouse': warehouse_dummy.id
        }
        self.warehouse_data = {
            'description': 'This is for testing'
        }
        self.dummy_warehouse_data = {
            'description': 'x'*255
            }
        self.dummy_inventory_data = {
            'stock': 10000000*1000000,
            'warehouse': warehouse_dummy.id
        }
        self.wrong_inventory_data = {
            'stock': 'test_string',
            'warehouse': warehouse_dummy.id
        }
        self.false_inventory_data = {
            'stock': 3000.00,
        }
        self.false_w_inventory_data = {
            'stock': 3000.00,
            'warehouse': 20
        }
        self.correct_whs_data_update = {
            'status': False
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
