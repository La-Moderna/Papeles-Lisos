"""Serializer for inventory API."""


from django.core.exceptions import ValidationError

from inventories.models import Inventory
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
            'warehouse_name',
            'description',
            'company'
        ]


class RetrieveWarehouseSerializer(serializers.ModelSerializer):
    """Serializer to retrieve warehouse"""

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'warehouse_name',
            'description',
            'company'
        ]


class UpdateWarehouseSerializer(serializers.Serializer):

    description = serializers.CharField(max_length=100)

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
    stock = serializers.DecimalField(max_digits=15, decimal_places=2)

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
            'warehouse'
        ]
