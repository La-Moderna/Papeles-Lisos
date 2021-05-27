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

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'company_id': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


router.register(
    r'companies',
    CompanyViewSet,
    'company'
)
