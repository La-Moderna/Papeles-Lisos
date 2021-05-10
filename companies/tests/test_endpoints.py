# Models
from companies.models import Company
from companies.serializers import CompanySerializer

# Django
from django.urls import reverse

# Django Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from utils.tokens import create_token


class CompanyTestEndpoints(APITestCase):
    def setUp(self):
        # Create User
        self.user = User.objects.create_user(
            email='a01365832@itesm.mx',
            password="123456789"
        )
        self.token = create_token(self.user)

        # Create Data
        self.company_1 = Company.objects.create(company=222, name="Ejemplo 1")
        self.company_2 = Company.objects.create(company=333, name="Ejemplo 2")
        self.company_3 = Company.objects.create(company=444, name="Ejemplo 3")
        self.company_4 = Company.objects.create(company=555, name="Ejemplo 3")

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
            reverse('company-detail', args=[self.company_3.company])
        )

        # Check Correct Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check Correct Data
        serializer = Company.objects.get(company=self.company_3.company)
        serializer = CompanySerializer(serializer)

        self.assertEqual(serializer.data, response.data)

    def test_create_companies(self):
        # Company Data
        company_data = {
            "company": 777,
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
        Company.objects.get(company=company_data['company'])
