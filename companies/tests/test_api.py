# Models
from companies.models import Company
from companies.serializers import CompanySerializer

# Django
from django.urls import reverse

# Django Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class CompanyTestEndpoints(APITestCase):
    def setUp(self):
        # Create User
        self.user = User.objects.create(
            email='user@test.com',
            name='Tester',
        )
        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

        # Create Data
        self.company_1 = Company.objects.create(
            id='222',
            name="Ejemplo 1"
        )

        self.company_2 = Company.objects.create(
            id='333',
            name="Ejemplo 2"
        )

        self.company_3 = Company.objects.create(
            id='444',
            name="Ejemplo 3"
        )

        self.company_4 = Company.objects.create(
            id='555',
            name="Ejemplo 3"
        )

        # Login
        data = {
            "email": self.user.email,
            "password": self.password
        }
        response = self.client.post(
            reverse('auth-list'),
            data
        )

        # Save Token
        self.token = response.data['token']

    # Test Correct Inputs #

    def test_get_companies(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # self.client.login(email=self.user.email, password=self.user.password)

        # Get all companies
        response = self.client.get(reverse('company-list'))

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check Correct Data
        serializer = Company.objects.all()
        serializer = CompanySerializer(serializer, many=True)

        self.assertEqual(serializer.data, response.data)

    def test_get_one_company(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # self.client.login(email=self.user.email, password=self.user.password)

        # Get all companies
        response = self.client.get(
            reverse('company-detail', args=[self.company_3.id])
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check Correct Data
        serializer = Company.objects.get(id=self.company_3.id)
        serializer = CompanySerializer(serializer)

        self.assertEqual(serializer.data, response.data)

    def test_create_companies(self):
        # Company Data
        company_data = {
            "id": "777",
            "name": "Ejemplo 7"
        }

        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # self.client.login(email=self.user.email, password=self.user.password)

        # Get all companies
        response = self.client.post(reverse('company-list'), company_data)

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Validate Company
        Company.objects.get(id=company_data['id'])

    def test_update_companies(self):
        # Company Data
        company_data = {
            "name": "Ejemplo 2 Update"
        }

        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Get all companies
        response = self.client.patch(
            reverse('company-detail', kwargs={'pk': '222'}),
            company_data
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check Correct Data
        company_retrive = Company.objects.get(id='222')

        self.assertEqual(company_data['name'], company_retrive.name)

    def test_delete_companies(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # self.client.login(email=self.user.email, password=self.user.password)

        # Get all companies
        response = self.client.delete(
            reverse('company-detail',  kwargs={'pk': '222'})
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test No Authentication #

    def test_get_companies_no_authentication(self):
        # Get all companies
        response = self.client.get(reverse('company-list'))

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_one_company_no_authentication(self):
        # Get all companies
        response = self.client.get(
            reverse('company-detail', args=[self.company_3.id])
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_companies_no_authentication(self):
        # Company Data
        company_data = {
            "id": "777",
            "name": "Ejemplo 7"
        }

        # Get all companies
        response = self.client.post(reverse('company-list'), company_data)

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_companies_no_authentication(self):
        # Get all companies
        response = self.client.delete(
            reverse('company-detail',  kwargs={'pk': '222'})
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test Invalid Arguments #

    def test_get_one_company_invalid_id(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Get all companies
        response = self.client.get(
            reverse('company-detail', args=[{'id': '000'}])
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_companies_none_values(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Company Data
        company_data = {
            "id": '',
            "name": ''
        }

        # Get all companies
        response = self.client.post(reverse('company-list'), company_data)

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_companies_none_name(self):
        # Authenticate with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Company Data
        company_data = {
            "id": '1234',
            "name": ''
        }

        # Get all companies
        response = self.client.post(reverse('company-list'), company_data)

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_companies_none_id(self):
            # Authenticate with token
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

            # Company Data
            company_data = {
                "id": '',
                "name": 'La moderna'
            }

            # Get all companies
            response = self.client.post(reverse('company-list'), company_data)

            # Check Correct Response
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
