from django.urls import reverse

from orders.models import Authorization

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

        self.auth1 = Authorization.objects.create(vta=True)
        self.auth2 = Authorization.objects.create(
            vta=True,
            cst=True,
            suaje=True
        )
        self.auth3 = Authorization.objects.create()
