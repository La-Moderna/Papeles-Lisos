from clients.models import Agent, Balance, Client, PriceList

from companies.models import Company

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from inventories.models import Item

from clients.utils import load_agents, load_balances, load_clients, load_priceList

from rest_framework import serializers


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""

    class Meta:
        model = Agent
        fields = ('__all__')


class CompanySlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            print(data)
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail(
                'does_not_exist',
                slug_name=self.slug_field,
                value=smart_text(data)
            )
        except (TypeError, ValueError):
            self.fail('invalid')


class CreateAgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""
    company = CompanySlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.all()
    )

    class Meta:
        model = Agent
        fields = [
            'representant',
            'company'
        ]


class RetrieveAgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent Model."""

    company = serializers.SlugRelatedField(
        read_only=True,
        slug_field='company_id'
    )

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


class LoadBalanceSerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    delimiter = serializers.CharField()

    class Meta:
        model = Balance
        fields = (
            'file',
            'delimiter'
        )

    def create(self, validated_data):
        file = validated_data.get('file')
        delimiter = validated_data.get('delimiter')

        load_balances(file, delimiter)

        return validated_data



class LoadAgentSerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    delimiter = serializers.CharField()

    class Meta:
        model = Agent
        fields = (
            'file',
            'delimiter'
        )

    def create(self, validated_data):
        file = validated_data.get('file')
        delimiter = validated_data.get('delimiter')

        load_agents(file, delimiter)

        return validated_data


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


class LoadClientSerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    delimiter = serializers.CharField()

    class Meta:
        model = Client
        fields = (
            'file',
            'delimiter'
        )

    def create(self, validated_data):
        file = validated_data.get('file')
        delimiter = validated_data.get('delimiter')

        load_clients(file, delimiter)

        return validated_data


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


class LoadPriceListSerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    delimiter = serializers.CharField()

    class Meta:
        model = PriceList
        fields = (
            'file',
            'delimiter'
        )

    def create(self, validated_data):
        file = validated_data.get('file')
        delimiter = validated_data.get('delimiter')

        load_priceList(file, delimiter)

        return validated_data
