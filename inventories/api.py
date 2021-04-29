
# """User API."""
# from django.shortcuts import get_object_or_404


from inventories import serializers
from inventories.models import Warehouse
from inventories.models import Inventory


from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.mixins import BaseGenericViewSet

from app.urls import router


class WarehouseViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet,
                       BaseGenericViewSet):
    """Manage Creation of a Warehouse"""

    serializer_class = serializers.WarehouseSerializer
    retrieve_serializer_class = serializers.RetrieveWarehouseSerializer
    permission_classes = [AllowAny]

    queryset = Warehouse.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, action='retrieve')
        return Response(serializer.data)

    # dar de baja almacen --> Se tiene que eliminar o solo cambiar su status?


class InventoryViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet,
                       BaseGenericViewSet
                       ):
    serializer_class = serializers.InventorySerializer
    retrieve_serializer_class = serializers.RetrieveInventorySerializer
    permission_classes = [AllowAny]

    queryset = Inventory.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, action='retrieve')
        return Response(serializer.data)

    # dar de baja inventario --> Se tiene que eliminar
    # o solo cambiar su status?


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
