# Create your views here.
from clients import serializers

from rest_framework import mixins, viewsets

from utils.mixins import BaseGenericViewSet

from app.urls import router


class AgentViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet,
                   BaseGenericViewSet):
    """Manage Agents."""
    serializer_class = serializers.AgentSerializer


class BalanceViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):
    """Manage Balance."""
    serializer_class = serializers.BalanceSerializer


router.register(
    r'clients/agents',
    AgentViewSet,
    basename="agent"
)

router.register(
    r'clients/balance',
    BalanceViewSet,
    basename="balance"
)
