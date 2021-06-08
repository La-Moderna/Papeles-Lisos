from companies.models import Company
from companies.utils import load_companies

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
            'company_id',
            'name'
        ]


class CreateCompanySerializer(serializers.ModelSerializer):

    def validate_name(self, name):
        if len(name) < 3:
            raise ValidationError('Name must have at least three characters')

        return name

    def validate_company_id(self, company_id):
        if len(company_id) < 1:
            raise ValidationError(
                'Company_id must have at least one character'
            )

        return company_id

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = [
            'company_id',
            'name'
        ]
<<<<<<< HEAD


class UpdateCompanySerializer(serializers.Serializer):

    id = serializers.CharField(max_length=4)
    name = serializers.CharField(max_length=70)

    def validate_name(self, name):
        if len(name) < 3:
            raise ValidationError('Name must have at least three characters')


class LoadCompanySerializer(serializers.ModelSerializer):

    file = serializers.FileField()
    delimiter = serializers.CharField()

    class Meta:
        model = Company
        fields = (
            'file',
            'delimiter'
        )

    def create(self, validated_data):
        file = validated_data.get('file')
        delimiter = validated_data.get('delimiter')

        load_companies(file, delimiter)

        return validated_data
=======
>>>>>>> d5f064d085e43a11b8f92c9861f286de624d0baa
