from companies.models import Company

from django.urls import reverse

from inventories.models import Item

from rest_framework.test import APITestCase

from users.models import User


class AuthorizationAPITestCase(APITestCase):
    """ Basic tests"""
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

        response = self.client.post(
            reverse('auth-list'),
            data
        )

        self.token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # self.auth1 = Authorization.objects.create(vta=True)
        # self.auth2 = Authorization.objects.create(
        #     vta=True,
        #     cst=True,
        #     suaje=True
        # )
        # self.auth3 = Authorization.objects.create()

        self.company = Company.objects.create(company_id="222",
                                              name="Papeles de Toluca")

        self.item = Item.objects.create(
            item_id="20012020",
            description="CAJA CARTÓN DMOX-3 1/2",
            udVta="MIL",
            access_key="44",
            standar_cost=2.4632,
            company=self.company)

        # self.order = Order.objects.create(
        #     item_id=self.item.item_id,
        #     cantidad=100,
        #     obsOrder="Ninguna",
        #     fechaOrden="24/04/2021",
        #     fechaSolicitada="05/05/2021"
        # )
        self.order_data = {
            "item_id": self.item.item_id,
            "cantidad": 100,
            "obsOrder": "Ninguna",
            "fechaOrden": "24/04/2021",
            "fechaSolicitada": "05/05/2021"
        }
        self.update_auth_1 = {
            "vta": True
        }

    def test_change_authorization_with_token_success(self):
        """Test succeeds to change status with correct data"""

        res_pre = self.client.post(reverse('order-list'), self.order_data)

        if res_pre.status_code == 201:
            order_id = res_pre.data['ordenCompra']
            res = self.client.patch(reverse(
                'auth-order-detail',
                kwargs={'pk': str(order_id)}),
                self.update_auth_1)
            self.assertEquals(res.status_code, 200)

    def test_change_authorization_without_token_fails(self):
        """Test fails to change status without token"""
        client = self.client
        client.credentials(HTTP_AUTHORIZATION='Credentials')
        res_pre = client.post(reverse('order-list'), self.order_data)

        self.assertEquals(res_pre.status_code, 401)
