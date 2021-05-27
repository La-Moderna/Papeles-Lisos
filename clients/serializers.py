from clients.models import Agent
from clients.models import Balance

from rest_framework import serializers


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""

    class Meta:
        model = Agent
        fields = ('__all__')


class CreateAgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""

    class Meta:
        model = Agent
        fields = [
            'representant',
            'company'
        ]


class RetrieveAgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""

    class Meta:
        model = Agent
        fields = [
            'representant',
            'company'
        ]


class BalanceSerializer(serializers.ModelSerializer):
    """Serializer for Balance Model."""

    class Meta:
        model = Balance
        fields = ('__all__')


class CreateBalanceSerializer(serializers.ModelSerializer):
    """Serializer for Balance Model."""

    class Meta:
        model = Balance
        fields = [
            'order_balance',
            'facture_balance',
            'company'
        ]


class RetrieveBalanceSerializer(serializers.ModelSerializer):
    """Serializer for Balance Model."""

    class Meta:
        model = Balance
        fields = [
            'order_balance',
            'facture_balance',
            'company'
        ]
