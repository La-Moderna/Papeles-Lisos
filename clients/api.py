# Create your views here.
from clients import models, serializers

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


class AgentViewSet(ListModelMixin,
                   CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet,
                   BaseGenericViewSet):
    """Manage Agents."""

    serializer_class = serializers.AgentSerializer
    list_serializer_class = serializers.RetrieveAgentSerializer
    create_serializer_class = serializers.CreateAgentSerializer
    retrieve_serializer_class = serializers.RetrieveAgentSerializer
    update_serializer_class = serializers.CreateAgentSerializer

    queryset = models.Agent.objects.filter(is_active=True)


class BalanceViewSet(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):
    """Manage Balance."""

    serializer_class = serializers.BalanceSerializer
    list_serializer_class = serializers.RetrieveBalanceSerializer
    create_serializer_class = serializers.CreateBalanceSerializer
    retrieve_serializer_class = serializers.RetrieveBalanceSerializer
    update_serializer_class = serializers.CreateBalanceSerializer

    queryset = models.Balance.objects.filter(is_active=True)


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
