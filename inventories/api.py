from django.shortcuts import get_object_or_404

from inventories import models, serializers
from inventories.models import Inventory
from inventories.models import Warehouse

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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


class LoadItemViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet,
                           BaseGenericViewSet):
    """ViewSet to upload data from csv."""

    create_serializer_class = serializers.LoadItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, action='create')
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            data={"status": "created"},
            status=status.HTTP_201_CREATED
        )


class LoadWarehouseViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet,
                           BaseGenericViewSet):
    """ViewSet to upload data from csv."""

    create_serializer_class = serializers.LoadWarehouseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, action='create')
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)

        return Response(
            data={"status": "created"},
            status=status.HTTP_201_CREATED
        )


class LoadInventoryViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet,
                           BaseGenericViewSet):
    """ViewSet to upload data from csv."""

    create_serializer_class = serializers.LoadInventorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, action='create')
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)

        return Response(
            data={"status": "created"},
            status=status.HTTP_201_CREATED
        )
router.register(
    r'items/load',
    LoadItemViewSet,
    basename='load-items'
)
router.register(
    r'warehouses/load',
    LoadWarehouseViewSet,
    basename="load-warehouses",
)
router.register(
    r'inventories/load',
    LoadInventoryViewSet,
    basename="load-inventories",
)
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
    basename='item'
)
