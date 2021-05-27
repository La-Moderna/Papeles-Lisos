from django.shortcuts import get_object_or_404

from inventories import models, serializers
from inventories.models import Inventory
from inventories.models import Warehouse

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


class WarehouseViewSet(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin,
                       viewsets.GenericViewSet,
                       BaseGenericViewSet):
    """Manage Creation of a Warehouse"""

    serializer_class = serializers.WarehouseSerializer
    list_serializer_class = serializers.RetrieveWarehouseSerializer
    create_serializer_class = serializers.CreateWarehouseSerializer
    retrieve_serializer_class = serializers.RetrieveWarehouseSerializer
    update_serializer_class = serializers.CreateWarehouseSerializer

    queryset = Warehouse.objects.filter(is_active=True)


class InventoryViewSet(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin,
                       viewsets.GenericViewSet,
                       BaseGenericViewSet):

    serializer_class = serializers.InventorySerializer
    list_serializer_class = serializers.RetrieveInventorySerializer
    create_serializer_class = serializers.CreateInventorySerializer
    retrieve_serializer_class = serializers.RetrieveInventorySerializer
    update_serializer_class = serializers.CreateInventorySerializer

    queryset = Inventory.objects.filter(is_active=True)


class ItemViewSet(ListModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  viewsets.GenericViewSet,
                  BaseGenericViewSet):

    serializer_class = serializers.ItemSerializer
    create_serializer_class = serializers.CreateItemSerializer
    list_serializer_class = serializers.RetrieveItemSerializer
    retrieve_serializer_class = serializers.RetrieveItemSerializer
    update_serializer_class = serializers.CreateItemSerializer

    queryset = models.Item.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'item_id': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


router.register(
    r'inventories',
    InventoryViewSet,
    basename="inventories",
)
router.register(
    r'warehouses',
    WarehouseViewSet,
    basename="warehouses",
)
router.register(
    r'items',
    ItemViewSet,
    'item'
)
