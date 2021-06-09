from django.shortcuts import get_object_or_404

from orders import serializers
from orders.models import (
    Authorization,
    DeliverAddress,
    DeliveredQuantity,
    Invoice
)

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


class AreaStatusViewset(ListModelMixin,
                        viewsets.GenericViewSet,
                        BaseGenericViewSet):
    serializer_class = serializers.AuthorizationSerializer
    list_serializer_class = serializers.AuthorizationSerializer

    # Missing filter with Orders that has salesOrder or inProgress
    queryset = Authorization.objects.all()

    # Missing check if user has rol of VTA or AGE
    # Missing order filter (all, in progress, processed)
    def list(self, request, *args, **kwargs):
        return super(AreaStatusViewset, self).list(request, *args, **kwargs)


class DeliveredQuantityViewset(ListModelMixin,
                               CreateModelMixin,
                               RetrieveModelMixin,
                               UpdateModelMixin,
                               DestroyModelMixin,
                               viewsets.GenericViewSet,
                               BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.DeliveredQuantitySerializer
    list_serializer_class = serializers.CustomDeliveredQuantitySerializer
    create_serializer_class = serializers.CustomDeliveredQuantitySerializer
    retrieve_serializer_class = serializers.CustomDeliveredQuantitySerializer
    update_serializer_class = serializers.CustomDeliveredQuantitySerializer

    queryset = DeliveredQuantity.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'order': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class InvoiceViewset(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.InvoiceSerializer
    list_serializer_class = serializers.CustomInvoiceSerializer
    create_serializer_class = serializers.CustomInvoiceSerializer
    retrieve_serializer_class = serializers.CustomInvoiceSerializer
    update_serializer_class = serializers.CustomInvoiceSerializer

    queryset = Invoice.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'invoice_number': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class DeliverAddressViewset(ListModelMixin,
                            CreateModelMixin,
                            RetrieveModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin,
                            viewsets.GenericViewSet,
                            BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.DeliverAddressSerializer
    list_serializer_class = serializers.RetrieveDeliverAddressSerializer
    create_serializer_class = serializers.CustomDeliverAddressSerializer
    retrieve_serializer_class = serializers.RetrieveDeliverAddressSerializer
    update_serializer_class = serializers.CustomDeliverAddressSerializer

    queryset = DeliverAddress.objects.filter(is_active=True)


router.register(
    r'order/status',
    AreaStatusViewset,
    'auth-order'
)

router.register(
    r'delivered-quantities',
    DeliveredQuantityViewset,
    basename='delivered-quantity'
)

router.register(
    r'deliver-addresses',
    DeliverAddressViewset,
    basename='deliver-address'
)
