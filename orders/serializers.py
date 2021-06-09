from clients.models import Client

from companies.models import Company

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from inventories.models import Item

from orders.models import (
    Authorization,
    DeliverAddress,
    DeliveredQuantity,
    Invoice
)

from rest_framework import serializers


# Missing Order field
class AuthorizationSerializer(serializers.ModelSerializer):
    """Serializer for Authorization"""

    class Meta:
        """Define the class behavior"""

        model = Authorization
        fields = [
            'vta',
            'cst',
            'suaje',
            'grabado',
            'pln',
            'ing',
            'cxc',
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


class DeliveredQuantitySerializer(serializers.ModelSerializer):
    """Serializer for DeliveredQuantity Model"""

    class Meta:
        """Define the class behavior"""

        model = DeliveredQuantity
        fields = '__all__'


class CustomDeliveredQuantitySerializer(serializers.ModelSerializer):
    """Custom Serializer for DeliveredQuantity Model"""
    company = SlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.filter(is_active=True)
    )
    item = SlugRelatedField(
        slug_field='item_id',
        queryset=Item.objects.filter(is_active=True)
    )

    class Meta:
        """Define the class behavior"""

        model = DeliveredQuantity
        fields = [
            'company',
            'order',
            'position',
            'mov_date',
            'time',
            'sequence',
            'reg_type',
            'quantity',
            'item'
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice Model"""

    class Meta:
        """Define the class behavior"""

        model = Invoice
        fields = '__all__'


class CustomInvoiceSerializer(serializers.ModelSerializer):
    """Custom Serializer for Invoice Model"""
    company = SlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.filter(is_active=True)
    )
    item = SlugRelatedField(
        slug_field='item_id',
        queryset=Item.objects.filter(is_active=True)
    )
    client = SlugRelatedField(
        slug_field='client_id',
        queryset=Client.objects.filter(is_active=True)
    )

    class Meta:
        """Define the class behavior"""

        model = Invoice
        fields = [
            'company',
            'invoice_number',
            'position',
            'delivery',
            'trans_type',
            'item',
            'invoice_date',
            'client'
        ]


class DeliverAddressSerializer(serializers.ModelSerializer):
    """Serializer for DeliverAddress Model"""

    class Meta:
        """Define the class behavior"""

        model = DeliverAddress
        fields = '__all__'


class CustomDeliverAddressSerializer(serializers.ModelSerializer):
    """Cuistom Serializer for DeliverAddress Model"""
    company = SlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.filter(is_active=True)
    )
    client = SlugRelatedField(
        slug_field='client_id',
        queryset=Client.objects.filter(is_active=True)
    )

    class Meta:
        """Define the class behavior"""

        model = DeliverAddress
        fields = [
            'company',
            'client',
            'del_address',
            'nameA',
            'nameB',
            'nameC',
            'nameD',
            'nameE',
            'postal_code',
            'route_code',
            'country',
            'rfc',
        ]


class RetrieveDeliverAddressSerializer(serializers.ModelSerializer):
    """Serializer to LIst or Retrieve DeliverAddress Model"""
    company = SlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.filter(is_active=True)
    )
    client = SlugRelatedField(
        slug_field='client_id',
        queryset=Client.objects.filter(is_active=True)
    )

    class Meta:
        """Define the class behavior"""

        model = DeliverAddress
        fields = [
            'id',
            'company',
            'client',
            'del_address',
            'nameA',
            'nameB',
            'nameC',
            'nameD',
            'nameE',
            'postal_code',
            'route_code',
            'country',
            'rfc',
        ]
