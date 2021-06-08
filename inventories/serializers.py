from companies.models import Company

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.encoding import smart_text

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
