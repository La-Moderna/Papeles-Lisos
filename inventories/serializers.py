from django.core.exceptions import ValidationError

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


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        """Define the class behavior"""

        model = Item
        fields = '__all__'


class RetrieveItemSerializer(serializers.ModelSerializer):
    """Serializer to retrieve Item"""

    class Meta:
        """Define the class behavior"""

        model = Item
        fields = [
            'id',
            'description',
            'udVta',
            'access_key',
            'standar_cost',
            'company'
        ]


class UpdateWarehouseSerializer(serializers.ModelSerializer):

    def validate_description(self, description):
        if len(description) < 3:
            raise ValidationError('Description must have at least three chars')


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


class UpdateInventorySerializer(serializers.Serializer):

    def validate_stock(self, stock):
        if stock < 0:
            raise ValidationError("Stock must be positive")


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


class CreateItemSerializer(serializers.ModelSerializer):
    """Serializer to retrieve Item"""

    def validate_id(self, id):
        if len(id) < 1:
            raise ValidationError('Id must have at least one characters')

        return id

    class Meta:
        """Define the class behavior"""

        model = Item
        fields = [
            'id',
            'description',
            'udVta',
            'access_key',
            'standar_cost',
            'company'
        ]
