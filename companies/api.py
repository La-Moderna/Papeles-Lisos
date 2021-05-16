from companies import models, serializers

from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from utils.mixins import (
    BaseGenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)

from app.urls import router


class CompanyViewSet(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):

    serializer_class = serializers.CompanySerializer
    list_serializer_class = serializers.RetrieveCompanySerializer
    create_serializer_class = serializers.CreateCompanySerializer
    retrieve_serializer_class = serializers.RetrieveCompanySerializer
    update_serializer_class = serializers.CreateCompanySerializer

    queryset = models.Company.objects.filter(is_active=True)

    def partial_update(self, request, *args, **kwargs):
        old_row = get_object_or_404(self.get_queryset(), pk=int(kwargs['pk']))

        new_row = super(
            CompanyViewSet,
            self
        ).partial_update(request, *args, **kwargs)

        if 'id' in request.data:
            id = request.data['id']

            if id is not None and id != old_row.pk:
                old_row.delete()

        return new_row


router.register(
    r'companies',
    CompanyViewSet,
    'company'
)
