import random

from inventories.models import Warehouse

from .test_setup import TestSetUp


class TestApi(TestSetUp):
    """ Basic tests"""
    def test_fails_to_register_without_data(self):
        res = self.client.post(self.create_inventory_url)
        self.assertEqual(res.status_code, 400)

    def test_gets_correctly_inventories(self):
        res = self.client.get(self.get_inventory_list_url)
        self.assertEqual(res.status_code, 200)

    def test_cannot_register_warehouse_without_data(self):
        res = self.client.post(self.create_warehouse_url)
        self.assertEqual(res.status_code, 400)

    def test_can_register_warehouse_with_data(self):
        res = self.client.post(self.create_warehouse_url, self.warehouse_data)
        self.assertEqual(res.status_code, 201)

    def test_can_retrieve_warehouses_list(self):
        res = self.client.get(self.get_warehouse_list_url)
        self.assertEqual(res.status_code, 200)

    def test_register_correctly_with_data(self):
        res = self.client.post(self.create_inventory_url, self.inventory_data)
        self.assertEqual(res.status_code, 201)

    # test to get 1 existing warehouse
    def test_get_one_existing_warehouse(self):

        warehouse_dummy = Warehouse(description='testing 1 object retrieval')
        warehouse_dummy.save()

        res = self.client.get(
            self.get_warehouse_list_url+"/"+str(warehouse_dummy.id)
        )
        self.assertEqual(res.status_code, 200)

    # test to get 1 non existing warehouse
    def test_fails_to_get_non_existing_warehouse(self):
        res = self.client.get(
            self.get_warehouse_list_url+"/"+str(random.randint(1, 10)*5356)
            )
        self.assertEqual(res.status_code, 404)

    # test to get 1 existing inventory
    def test_get_one_existing_inventory(self):
        res_create = self.client.post(
            self.create_inventory_url,
            self.inventory_data)
        aux = res_create.json()
        if res_create.status_code == 201:
            res = self.client.get(
                self.get_inventory_list_url+"/"+str(aux['id'])
            )
            self.assertEqual(res.status_code, 200)

    # test to get 1 non existing inventory
    def test_fails_to_get_non_existing_inventory(self):
        res = self.client.get(
            self.get_warehouse_list_url+str(random.randint(1, 10)*5536)
            )
        self.assertEqual(res.status_code, 404)

    # test to register a warehouse with wrong data type
    def test_fails_to_register_warehouse_with_larger_data(self):
        res = self.client.post(
            self.create_warehouse_url,
            self.dummy_warehouse_data
        )
        self.assertEqual(res.status_code, 400)

    # test to register an inventory with wrong data type
    def test_fails_to_register_inventory_with_enourmus_number_type(self):
        res = self.client.post(
            self.create_inventory_url,
            self.dummy_inventory_data
        )
        self.assertEqual(res.status_code, 400)

    # test to try to register an inventory with wrong stock data type
    def test_fails_to_register_inventory_with_wrong_type(self):
        res = self.client.post(
            self.create_inventory_url,
            self.wrong_inventory_data
        )
        self.assertEqual(res.status_code, 400)

    # test to try to register an inventory with a non existing foreign key
    def test_fails_register_inventory_not_foreign_key(self):
        res = self.client.post(
            self.create_inventory_url,
            self.false_inventory_data
        )
        self.assertEqual(res.status_code, 400)

    def test_fails_register_inventory_false_foreign_key(self):
        res = self.client.post(
            self.create_inventory_url,
            self.false_w_inventory_data
        )
        self.assertEqual(res.status_code, 400)

    # test to try to update a field correctly --> No reverse match
    # def test_updates_status_warehouse_correctly(self):
    #     res = self.client.patch(
    #         self.update_warehouse_url+"/"+str(7),
    #         self.correct_whs_data_update
    #     )
    #     print(res.data)
    #     self.assertEqual(res.status_code, 200)

    # update not existing inventory

    # update not existing wareohuse

    # update with wrong data type wareohuse

    # update with wrong data type inventory
