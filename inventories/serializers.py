from django.core.exceptions import ValidationError

from inventories.models import Item

from inventories.utils import load_items

from rest_framework import serializers


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

class LoadItemSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    delimiter = serializers.CharField()

    class Meta:
        model = Item
        fields = (
            'file',
            'delimiter'
        )

    def create(self, validated_data):
        file = validated_data.get('file')
        delimiter = validated_data.get('delimiter')

        load_items(file, delimiter)

        return validated_data
