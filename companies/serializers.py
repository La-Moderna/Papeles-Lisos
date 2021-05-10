from companies.models import Company

from rest_framework import serializers


class CompanySerializer(serializers.Serializer):
    """Serializer for Company"""

    class Meta:
        """Define the class behavior"""

        model = Company
        fields = '__all__'
