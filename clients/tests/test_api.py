from clients.models import Agent, Balance

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from utils.tokens import create_token


class AgentTestEndpoints(APITestCase):
    def setUp(self):
        # Create User
        self.user = User.objects.create_user(email='A01363677@itesm.mx',
                                             password="asdf")
        self.token = create_token(self.user)

        # Create Data
        self.agent = Agent.objects.create(representant="edmond")

    def test_create_agents(self):
        agent_data = {
            "representant": "Edmond"
        }

        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Get all agents
        response = self.client.post(reverse('agent-list'), agent_data)

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Validate Company
        Agent.objects.get(representant=agent_data['representant'])


class BalanceTestEndpoints(APITestCase):
    def setUp(self):
        # Create User
        self.user = User.objects.create_user(email='A01363677@itesm.mx',
                                             password="asdf")
        self.token = create_token(self.user)

        # Create Data
        self.balance = Balance.objects.create(order_balance="1500",
                                              facture_balance="1450")

    def test_create_Balance(self):
        balance_data = {
            "order_balance": "1000",
            "facture_balance": "1400"
        }

        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Get all balances
        response = self.client.post(reverse('balance-list'), balance_data)

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Validate Company
        Balance.objects.get(order_balance=balance_data['order_balance'])
