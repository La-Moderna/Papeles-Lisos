from clients.models import Agent, Balance, Client, PriceList

from companies.models import Company

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from inventories.models import Item

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


class SlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail(
                'does_not_exist',
                slug_name=self.slug_field,
                value=smart_text(data)
            )
        except (TypeError, ValueError):
            self.fail('invalid')


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client Model."""

    class Meta:
        model = Client
        fields = '__all__'


class CustomClientSerializer(serializers.ModelSerializer):
    """Custom Serializer for Client Model."""
    company = SlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.filter(is_active=True)
    )
    price_lists = SlugRelatedField(
        slug_field='price_list_id',
        many=True,
        queryset=PriceList.objects.filter(is_active=True)
    )

    class Meta:
        model = Client
        fields = [
            'company',
            'client_id',
            'nameA',
            'nameB',
            'status',
            'agent',
            'analist',
            'currency',
            'credit_lim',
            'price_lists',
            'warehouse'
        ]


class PriceListSerializer(serializers.ModelSerializer):
    """Serializer for PriceList Model."""

    class Meta:
        model = PriceList
        fields = '__all__'


class CustomPriceListSerializer(serializers.ModelSerializer):
    """Custom Serializer for PriceList Model."""
    company = SlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.filter(is_active=True)
    )

    item = SlugRelatedField(
        slug_field='item_id',
        queryset=Item.objects.filter(is_active=True)
    )

    def validate_discount(self, value):
        if 0 <= value <= 100:
            return value
        raise serializers.ValidationError(
            "Discount must be between 0 and 100."
        )

    class Meta:
        model = PriceList
        fields = [
            'price_list_id',
            'company',
            'item',
            'discount_level',
            'cantOImp',
            'price',
            'discount',
            'start_date',
            'end_date'
        ]
