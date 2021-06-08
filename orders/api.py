from orders import models, serializers

from rest_framework import viewsets

from utils.mixins import (
    BaseGenericViewSet,
    ListModelMixin,
)

from app.urls import router


class AreaStatusViewset(ListModelMixin,
                        viewsets.GenericViewSet,
                        BaseGenericViewSet):
    serializer_class = serializers.AuthorizationSerializer
    list_serializer_class = serializers.AuthorizationSerializer

    # Missing filter with Orders that has salesOrder or inProgress
    queryset = models.Authorization.objects.all()

    # Missing check if user has rol of VTA or AGE
    # Missing order filter (all, in progress, processed)
    def list(self, request, *args, **kwargs):
        return super(AreaStatusViewset, self).list(request, *args, **kwargs)


router.register(
    r'order/status',
    AreaStatusViewset,
    'auth-order'
)
