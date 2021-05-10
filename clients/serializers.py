from clients.models import Agent
from clients.models import Balance

from rest_framework import serializers


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""

    class Meta:
        model = Agent
        fields = ('__all__')


class BalanceSerializer(serializers.ModelSerializer):
    """Serializer for Balance Model."""

    class Meta:
        model = Balance
        fields = ('__all__')
