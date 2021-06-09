from django.core.exceptions import ObjectDoesNotExist

from clients.utils import load_agents
from django.utils.encoding import smart_text

from clients.models import Agent, Balance
from companies.models import Company

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
