from companies.models import Company
from companies.serializers import CompanySerializer

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class CompaniesAPITestCase(APITestCase):
    """Test /companies endpoint."""
    def setUp(self):
        self.user = User.objects.create(
            email='user@test.com',
            name='Tester',
        )
        self.password = 'Tester_123'
        self.user.set_password(self.password)
        self.user.save()

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

    def test_list_companies(self):
        '''Test valid list of companies'''
        response = self.client.get(reverse('company-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = Company.objects.all()
        serializer = CompanySerializer(serializer, many=True)

        self.assertDictContainsSubset(
            {
                'id': self.company_1.id,
                'name': self.company_1.name
            }, response.data[0])

        self.assertDictContainsSubset(
            {
                'id': self.company_2.id,
                'name': self.company_2.name
            }, response.data[1])

        self.assertDictContainsSubset(
            {
                'id': self.company_3.id,
                'name': self.company_3.name
            }, response.data[2])

        self.assertDictContainsSubset(
            {
                'id': self.company_4.id,
                'name': self.company_4.name
            }, response.data[3])

    def test_retrieve_company(self):
        '''Test valid retrive company with a valid id'''
        response = self.client.get(
            reverse('company-detail', args=[self.company_3.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'id': self.company_3.id,
                'name': self.company_3.name
            }, response.data)

    def test_create_company(self):
        '''Test valid creation of company'''
        company_data = {
            "id": "777",
            "name": "Ejemplo 7"
        }

        response = self.client.post(reverse('company-list'), company_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        company = Company.objects.get(id=company_data['id'])
        self.assertEqual(company.name, company_data['name'])

    def test_partial_update_company_name(self):
        '''Test valid update company name with an existing id'''
        company_data = {
            "name": "Ejemplo 2 Update"
        }

        response = self.client.patch(
            reverse('company-detail', kwargs={'pk': '222'}),
            company_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        company_retrive = Company.objects.get(id='222')

        self.assertEqual(company_data['name'], company_retrive.name)

    def test_partial_update_company_is_active(self):
        '''Test not valid update of is_active'''
        company_data = {
            "is_active": False
        }

        response = self.client.patch(
            reverse('company-detail', kwargs={'pk': self.company_2.id}),
            company_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'id': self.company_2.id,
                'name': self.company_2.name
            },
            response.data
        )

    def test_partial_update_company_id(self):
        '''Test not valid update of is_active'''
        company_data = {
            "id": '9999'
        }

        old_id = self.company_2.id

        response = self.client.patch(
            reverse('company-detail', kwargs={'pk': self.company_2.id}),
            company_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(
            {
                'id': company_data['id'],
                'name': self.company_2.name
            },
            response.data
        )

        list = Company.objects.filter(id=old_id)

        self.assertEqual(len(list), 0)

    def test_destroy_company(self):
        '''Test valid destroy company, updating the is_active value'''
        response = self.client.delete(
            reverse('company-detail',  kwargs={'pk': '222'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        company = Company.objects.get(pk='222')
        self.assertEqual(company.is_active, False)

    def test_list_companies_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(reverse('company-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_company_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.get(
            reverse('company-detail', args=[self.company_3.id])
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_companies_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        company_data = {
            "id": "777",
            "name": "Ejemplo 7"
        }

        response = client.post(reverse('company-list'), company_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_companies_no_authentication(self):
        '''Test no valid request with incorrect credentials'''
        client = self.client
        client.credentials(
            HTTP_AUTHORIZATION='Credentials'
        )

        response = client.delete(
            reverse('company-detail',  kwargs={'pk': '222'})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_company_invalid_id(self):
        '''Test no valid retrieve request with invalid id'''
        response = self.client.get(
            reverse('company-detail', args=[{'id': '000'}])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_company_none_values(self):
        '''Test no valid create request with missing fields'''
        company_data = {}

        response = self.client.post(reverse('company-list'), company_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "id": [
                    "This field is required."
                ],
                "name": [
                    "This field is required."
                ]
            },
            response.data
        )

    def test_create_company_blank(self):
        '''Test no valid create request with blank fields'''
        company_data = {
            "id": '',
            "name": ''
        }

        response = self.client.post(reverse('company-list'), company_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertDictContainsSubset(
            {
                "id": [
                    "This field may not be blank."
                ],
                "name": [
                    "This field may not be blank."
                ]
            },
            response.data
        )
