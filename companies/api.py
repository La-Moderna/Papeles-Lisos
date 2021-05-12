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
    retrieve_serializer_class = serializers.RetriveCompanySerializer
    create_serializer_class = serializers.CreateCompanySerializer
    update_serializer_class = serializers.UpdateCompanySerializer
    queryset = models.Company.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        company_serializer = self.get_serializer(
            queryset,
            action='retrieve',
            many=True
        )

        return Response(company_serializer.data)

    def create(self, request, *args, **kwargs):
        company_serializer = self.get_serializer(
            data=request.data,
            action='create'
        )

        if company_serializer.is_valid():
            data = request.data

            id = data['id']
            name = data['name']

            company = models.Company.objects.create(
                id=id,
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

    def partial_update(self, request, pk=None):
        queryset = self.get_queryset()
        company_object = get_object_or_404(queryset, pk=pk)

        company_serializer = self.get_serializer(
            company_object,
            data=request.data,
            action='update',
            partial=True
        )

        if company_serializer.is_valid():
            company_object.name = request.data['name']
            company_object.save()
            return Response(company_serializer.data)

        else:
            return Response(
                company_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(user, action='retrieve')

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()
        company.is_active = False
        company.save()

        serializer = self.get_serializer(company)

        return Response(serializer.data)


router.register(
    r'companies',
    CompanyViewSet,
    'company'
)
