from django.shortcuts import get_object_or_404

from inventories import models, serializers

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.mixins import (
    BaseGenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from app.urls import router


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

    def partial_update(self, request, *args, **kwargs):
        old_row = get_object_or_404(self.get_queryset(), pk=int(kwargs['pk']))

        new_row = super(
            ItemViewSet,
            self
        ).partial_update(request, *args, **kwargs)

        if 'id' in request.data:
            id = request.data['id']

            if id is not None and id != old_row.pk:
                old_row.delete()

        return new_row


class LoadItemViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet,
                           BaseGenericViewSet):
    """ViewSet to upload data from csv."""

    create_serializer_class = serializers.LoadItemSerializer

    permission_classes = [AllowAny]

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
    r'items',
    ItemViewSet,
    basename='item'
)
