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


class AgentViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                   DestroyModelMixin, UpdateModelMixin,
                   viewsets.GenericViewSet,
                   BaseGenericViewSet):
    """Manage Agents."""
    serializer_class = serializers.AgentSerializer
    create_serializer_class = serializers.CreateAgentSerializer
    list_serializer_class = serializers.ListAgentSerializer
    retrieve_serializer_class = serializers.RetrieveAgentSerializer
    update_serializer_class = serializers.UpdateAgentSerializer

    queryset = models.Agent.objects.filter(is_active=True)


class BalanceViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                     DestroyModelMixin, UpdateModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):
    """Manage Balance."""
    serializer_class = serializers.BalanceSerializer
    create_serializer_class = serializers.CreateBalanceSerializer
    list_serializer_class = serializers.ListBalanceSerializer
    retrieve_serializer_class = serializers.RetrieveBalanceSerializer
    update_serializer_class = serializers.UpdateBalanceSerializer

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
