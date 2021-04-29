"""Serializer for inventory API."""

from inventories.models import Warehouse
from inventories.models import Inventory

from rest_framework import serializers


# class CreateInventorySerializer(serializers.Serializer):
#     """Serializer for CreateInventory API when POST method is used"""
#     company = serializers.CharField(required=True, max_length=4)
#     almacen = serializers.CharField(required=True, max_length=4)

#     def validate_almacen(self, value):
#         """Raise ValidationError if almacen already exists"""
#         if Inventory.objects.filter(almacen=value).exists():
#             raise serializers.ValidationError(
#                 "Inventory has already been registered"
#             )
#         else:
#             return value

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class RetrieveWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id',
            'description'
        ]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class RetrieveInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'id',
            'stock'
        ]
