from companies.models import Company

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.encoding import smart_text

from inventories.models import Inventory
from inventories.models import Item
from inventories.models import Warehouse

from rest_framework import serializers


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for warehouse"""
    class Meta:
        model = Warehouse
        fields = '__all__'


class CreateWarehouseSerializer(serializers.ModelSerializer):

    def validate_description(self, description):
        if(len(description) < 5):
            raise ValidationError("Description must have at least five chars")

        return description

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'name',
            'description',
            'company'
        ]


class RetrieveWarehouseSerializer(serializers.ModelSerializer):
    """Serializer to retrieve warehouse"""

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'name',
            'description',
            'company'
        ]


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory"""

    class Meta:
        model = Inventory
        fields = '__all__'


class RetrieveInventorySerializer(serializers.ModelSerializer):
    """"Serializer to retrieve inventory"""

    stock = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = Inventory
        fields = [
            'id',
            'stock'
        ]


class CreateInventorySerializer(serializers.ModelSerializer):
    """Serializer to create inventory"""

    stock = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = Inventory
        fields = [
            'id',
            'stock',
            'warehouse',
            'item'
        ]


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        """Define the class behavior"""

        model = Item
        fields = '__all__'


class RetrieveItemSerializer(serializers.ModelSerializer):
    """Serializer to retrieve Item"""
    company = serializers.SlugRelatedField(
        read_only=True,
        slug_field='company_id'
    )

    class Meta:
        """Define the class behavior"""

        model = Item
        fields = [
            'item_id',
            'description',
            'udVta',
            'access_key',
            'standar_cost',
            'company'
        ]


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


class CreateItemSerializer(serializers.ModelSerializer):
    """Serializer to retrieve Item"""
    company = CompanySlugRelatedField(
        slug_field='company_id',
        queryset=Company.objects.all()
    )

    def validate_id(self, item_id):
        if len(item_id) < 1:
            raise ValidationError('Id must have at least one characters')

        return item_id

    class Meta:
        """Define the class behavior"""

        model = Item
        fields = [
            'item_id',
            'description',
            'udVta',
            'access_key',
            'standar_cost',
            'company'
        ]
