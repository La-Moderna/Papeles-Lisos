from clients.models import Agent, Balance
from clients.serializers import AgentSerializer, BalanceSerializer

from companies.models import Company

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AgentAPITestCase(APITestCase):
    """Test/agents model."""
    def setUp(self):
        self.company = Company.objects.create(
            id='619',
            name="Ejemplo1"
        )
        self.user = User.objects.create(
            email='edmond@test.com',
            name='Tester',
        )
        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

        self.agent = Agent.objects.create(
            representant="edmond",
            company=self.company
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

    def test_create_agents(self):
        """Test /success create."""
        agent_data = {
            "representant": "Edmond",
            "company": self.company.id
        }

        response = self.client.post(reverse('agent-list'), agent_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        agent = Agent.objects.get(representant=agent_data['representant'])
        self.assertEqual(agent.representant, agent_data['representant'])

    def test_list_agents(self):
        '''Test valid list of agents'''
        response = self.client.get(reverse('agent-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = Agent.objects.all()
        serializer = AgentSerializer(serializer, many=True)

        self.assertDictContainsSubset(
            {
                'representant': self.agent.representant,
                'company': self.company.id
            }, response.data[0])

    def test_retrieve_agent(self):
        '''Test valid retrieve agent with a valid id'''
        response = self.client.get(
            reverse('agent-detail', args=[self.agent.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'representant': self.agent.representant,
                'company': self.company.id
            }, response.data)

    def test_partial_update_agent_is_active(self):
        '''Test not valid update of is_active'''
        agent_data = {
            "is_active": False
        }

        response = self.client.patch(
            reverse('agent-detail', kwargs={'pk': self.agent.id}),
            agent_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'representant': self.agent.representant,
            },
            response.data
        )

    def test_destroy_agent(self):
        '''Test valid destroy agent, updating the is_active value'''
        response = self.client.delete(
            reverse('agent-detail', kwargs={'pk': self.agent.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        agent = Agent.objects.get(id=self.agent.id)
        self.assertEqual(agent.is_active, False)

    def test_list_agents_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(reverse('agent-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_agent_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(
            reverse('agent-detail', args=[self.company.id])
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_agents_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        agent_data = {
            "representant": "Edmond",
            "company": "777"
        }

        response = client.post(reverse('agent-list'), agent_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_agents_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.delete(
            reverse('agent-detail',  kwargs={'pk': self.agent.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_agent_invalid_id(self):
        '''Test no valid retrieve request with invalid representant'''
        response = self.client.get(
            reverse('agent-detail', args=[{'representant': 'Edmond'}])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_agent_none_values(self):
        '''Test no valid create request with missing fields'''
        agent_data = {}

        response = self.client.post(reverse('agent-list'), agent_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "representant": [
                    "This field is required."
                ],
                "company": [
                    "This field is required."
                ]
            },
            response.data
        )

    def test_create_agent_blank(self):
        '''Test no valid create request with blank fields'''
        agent_data = {
            "representant": '',
            "company": ''
        }

        response = self.client.post(reverse('agent-list'), agent_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "representant": [
                    "This field may not be blank."
                ],
            },
            response.data
        )


class BalanceAPITestCase(APITestCase):
    """Test/balance model."""
    def setUp(self):
        self.company = Company.objects.create(
            id='619',
            name="Ejemplo1"
        )
        self.user = User.objects.create(
            email='edmond@test.com',
            name='Tester',
        )
        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

        self.balance = Balance.objects.create(
            order_balance="200",
            facture_balance="300",
            company=self.company
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

    def test_create_balance(self):
        """Test /success create."""
        balance_data = {
            "order_balance": "1200",
            "facture_balance": "1300",
            "company": self.company.id
        }

        response = self.client.post(reverse('balance-list'), balance_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        agent = Balance.objects.get(order_balance=balance_data
                                    ['order_balance'])
        self.assertEqual(agent.order_balance, balance_data['order_balance'])

    def test_list_balance(self):
        '''Test valid list of balance'''
        response = self.client.get(reverse('balance-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = Balance.objects.all()
        serializer = BalanceSerializer(serializer, many=True)

        self.assertDictContainsSubset(
            {
                'order_balance': self.balance.order_balance,
                'facture_balance': self.balance.facture_balance,
                'company': self.company.id
            }, response.data[0])

    def test_retrieve_balance(self):
        '''Test valid retrieve balance with a valid id'''
        response = self.client.get(
            reverse('balance-detail', args=[self.balance.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'order_balance': self.balance.order_balance,
                'facture_balance': self.balance.facture_balance,
                'company': self.company.id
            }, response.data)

    def test_partial_update_balance_is_active(self):
        '''Test not valid update of is_active'''
        balance_data = {
            "is_active": False
        }

        response = self.client.patch(
            reverse('balance-detail', kwargs={'pk': self.balance.id}),
            balance_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'order_balance': self.balance.order_balance,
                'facture_balance': self.balance.facture_balance
            },
            response.data
        )

    def test_destroy_balance(self):
        '''Test valid destroy balance, updating the is_active value'''
        response = self.client.delete(
            reverse('balance-detail', kwargs={'pk': self.balance.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        balance = Balance.objects.get(id=self.balance.id)
        self.assertEqual(balance.is_active, False)

    def test_list_balance_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(reverse('balance-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_balance_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(
            reverse('balance-detail', args=[self.company.id])
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_balance_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        balance_data = {
            'order_balance': self.balance.order_balance,
            'facture_balance': self.balance.facture_balance,
            "company": "777"
        }

        response = client.post(reverse('balance-list'), balance_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_balance_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.delete(
            reverse('balance-detail',  kwargs={'pk': self.balance.id})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_balance_invalid_id(self):
        '''Test no valid retrieve request with invalid representant'''
        response = self.client.get(
            reverse('balance-detail', args=[{'order_balance': '1500'}])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_balance_none_values(self):
        '''Test no valid create request with missing fields'''
        balance_data = {}

        response = self.client.post(reverse('balance-list'), balance_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "order_balance": [
                    "This field is required."
                ],
                "facture_balance": [
                    "This field is required."
                ],
                "company": [
                    "This field is required."
                ]
            },
            response.data
        )

    def test_create_balance_blank(self):
        '''Test no valid create request with blank fields'''
        balance_data = {
            "order_balance": '',
            "facture_balance": '',
            "company": ''
        }

        response = self.client.post(reverse('balance-list'), balance_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "order_balance": [
                    "This field may not be blank."
                ],
                "facture_balance": [
                    "This field may not be blank."
                ]
            },
            response.data
        )
