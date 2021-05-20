
# """User API."""
# from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404

from inventories import serializers
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
    create_serializer_class = serializers.CreateWarehouseSerializer
    list_serializer_class = serializers.WarehouseSerializer
    retrieve_serializer_class = serializers.RetrieveWarehouseSerializer
    update_serializer_class = serializers.CreateWarehouseSerializer

    queryset = Warehouse.objects.filter(is_active=True)

    def partial_update(self, request, *args, **kwargs):
        old_row = get_object_or_404(self.get_queryset(), pk=int(kwargs['pk']))

        new_row = super(
            WarehouseViewSet,
            self
        ).partial_update(request, *args, **kwargs)

        if 'id' in request.data:
            id = request.data['id']

            if id is not None and id != old_row.pk:
                old_row.delete()

        return new_row


class InventoryViewSet(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin,
                       viewsets.GenericViewSet,
                       BaseGenericViewSet):

    serializer_class = serializers.InventorySerializer
    retrieve_serializer_class = serializers.RetrieveInventorySerializer
    list_serializer_class = serializers.InventorySerializer
    create_serializer_class = serializers.InventorySerializer
    update_serializer_class = serializers.CreateInventorySerializer

    queryset = Inventory.objects.filter(is_active=True)

    def partial_update(self, request, *args, **kwargs):
        old_row = get_object_or_404(self.get_queryset(), pk=int(kwargs['pk']))

        new_row = super(
            InventoryViewSet,
            self
        ).partial_update(request, *args, **kwargs)

        if 'id' in request.data:
            id = request.data['id']

            if id is not None and id != old_row.pk:
                old_row.delete()

        return new_row


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
