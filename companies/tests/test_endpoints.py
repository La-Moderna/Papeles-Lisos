# # Django
# from django.urls import reverse
#
# # Django Rest Framework
# from rest_framework.test import APITestCase
# from rest_framework import status
#
# # Models
# from companies.models import Company
#
#
# class CompanyTestEndpoints(APITestCase):
#     def setUp(self):
#         self.company = Company.objects.create(
#             name="PELICULAS PLASTICAS SA DE CV"
#         )
#
#     def test_get_companies(self):
#         response = self.client.get(reverse('admin'))
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
