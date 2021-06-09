from clients import serializers
from clients.models import Agent, Balance, Client, PriceList

from django.shortcuts import get_object_or_404


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

    queryset = Agent.objects.filter(is_active=True)


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

    queryset = Balance.objects.filter(is_active=True)


class ClientViewset(ListModelMixin,
                    CreateModelMixin,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    viewsets.GenericViewSet,
                    BaseGenericViewSet):
    "Manage Clients"

    serializer_class = serializers.ClientSerializer
    list_serializer_class = serializers.CustomClientSerializer
    create_serializer_class = serializers.CustomClientSerializer
    retrieve_serializer_class = serializers.CustomClientSerializer
    update_serializer_class = serializers.CustomClientSerializer

    queryset = Client.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'client_id': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class PriceListViewset(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin,
                       viewsets.GenericViewSet,
                       BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.PriceListSerializer
    list_serializer_class = serializers.CustomPriceListSerializer
    create_serializer_class = serializers.CustomPriceListSerializer
    retrieve_serializer_class = serializers.CustomPriceListSerializer
    update_serializer_class = serializers.CustomPriceListSerializer

    queryset = PriceList.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'price_list_id': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


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

router.register(
    r'price-lists',
    PriceListViewset,
    basename="price-list"
)

router.register(
    r'clients',
    ClientViewset,
    basename="client"
)
