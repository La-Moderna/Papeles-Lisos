from companies.models import Company

from django.core.exceptions import ValidationError

from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company"""

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = '__all__'


class RetrieveCompanySerializer(serializers.ModelSerializer):
    """Serializer to retrieve Company"""

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = [
            'id',
            'name'
        ]


class CreateCompanySerializer(serializers.ModelSerializer):

    def validate_name(self, name):
        if len(name) < 3:
            raise ValidationError('Name must have at least Three character')

        return name

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = [
            'id',
            'name'
        ]


class UpdateCompanySerializer(serializers.Serializer):

    id = serializers.CharField(max_length=4)
    name = serializers.CharField(max_length=70)

    def validate_name(self, name):
        if len(name) < 3:
            raise ValidationError('Name must have at least Three character')
