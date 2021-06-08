from orders.models import Authorization

from rest_framework import serializers


# Missing Order field
class AuthorizationSerializer(serializers.ModelSerializer):
    """Serializer for Authorization"""

    class Meta:
        """Define the class behavior"""

        model = Authorization
        fields = [
            'vta',
            'cst',
            'suaje',
            'grabado',
            'pln',
            'ing',
            'cxc',
        ]
