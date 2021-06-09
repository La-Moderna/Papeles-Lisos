from orders.models import Authorization, OrderDetail, Order

from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    class Meta:
        """Define the class behavior"""

        model = Order
        fields = [
            'obsOrder',
            'ordenCompra',
            'fechaOrden',
            'fechaSolicitada'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""

    class Meta:
        """Define the class behavior"""

        model = Order
        fields = [
            'obsOrder',
            'fechaOrden',
            'fechaSolicitada'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order Detail"""
    item = serializers.SlugRelatedField(
        read_only=True,
        slug_field='item_id'
    )

    order = serializers.SlugRelatedField(
        read_only=True,
        slug_field='ordenCompra'
    )

    class Meta:
        """Define the class behavior"""

        model = OrderDetail
        fields = [
            'cantidad',
            'udvta',
            'precio',
            'posicion',
            'item',
            'order'
        ]


class UpdateOrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order Detail"""

    class Meta:
        """Define the class behavior"""

        model = OrderDetail
        fields = [
            'cantidad',
            'precio',
            'posicion'
        ]


class CreateOrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order Detail"""

    class Meta:
        """Define the class behavior"""

        model = OrderDetail
        fields = [
            'cantidad'
        ]


# Missing Order field
class AuthorizationSerializer(serializers.ModelSerializer):
    """Serializer for Authorization"""
    order = serializers.SlugRelatedField(
        read_only=True,
        slug_field='ordenCompra'
    )

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
            'order'
        ]
