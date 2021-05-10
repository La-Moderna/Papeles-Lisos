from companies import models, serializers

from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from utils.mixins import BaseGenericViewSet

from app.urls import router


class CompanyViewSet(mixins.CreateModelMixin,
                     viewsets.ViewSet,
                     BaseGenericViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        company_serializer = self.get_serializer(queryset, many=True)

        return Response(company_serializer.data)

    def create(self, request, *args, **kwargs):
        company_serializer = self.get_serializer(
            data=request.data
        )

        if company_serializer.is_valid():
            data = request.data

            company = data['company']
            name = data['name']

            company = models.Company.objects.create(
                company=company,
                name=name
            )

            company.save()

            return Response(
                company_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                company_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(user)

        return Response(serializer.data)


router.register(
    r'companies',
    CompanyViewSet,
    'company'
)
