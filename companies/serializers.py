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
