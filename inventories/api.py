from django.shortcuts import get_object_or_404

from inventories import models, serializers

from rest_framework import viewsets

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


router.register(
    r'items',
    ItemViewSet,
    'item'
)
