from companies.models import Company

from django.core.exceptions import ValidationError

from rest_framework import serializers


class CompanySerializer(serializers.Serializer):
    """Serializer for Company"""

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = '__all__'


class RetriveCompanySerializer(serializers.Serializer):
    """Serializer for Company"""

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = [
            'id',
            'name'
        ]


class CreateCompanySerializer(serializers.Serializer):

    id = serializers.CharField(max_length=4)
    name = serializers.CharField(max_length=70)
    is_active = serializers.BooleanField(default=True)

    def validate_id(self, id):
        if id == '':
            raise ValidationError('Id must have at least one character')

    def validate_name(self, name):
        if len(name) <= 3:
            raise ValidationError('Name must have at least Three character')


class UpdateCompanySerializer(serializers.Serializer):

    id = serializers.CharField(max_length=4)
    name = serializers.CharField(max_length=70)
    is_active = serializers.BooleanField(default=True)

    def validate_id(self, id):
        if id == '':
            raise ValidationError('Id must have at least one character')

    def validate_name(self, name):
        if len(name) <= 3:
            raise ValidationError('Name must have at least Three character')

    def validate_is_active(self, is_active):
        if (is_active is not True or is_active is not False):
            raise ValidationError('is_active must be a boolean value')

    def update(self, instance, validated_data):
        instance.id = validated_data.get(
            'id',
            instance.id
        )

        instance.name = validated_data.get(
            'name',
            instance.name
        )

        instance.is_active = validated_data.get(
            'is_active',
            instance.is_active
        )

        return instance
