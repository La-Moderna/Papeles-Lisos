from django.shortcuts import get_object_or_404

from inventories.models import Item

from orders import serializers
from orders.models import (
    Authorization,
    DeliverAddress,
    DeliveredQuantity,
    Invoice,
    Order,
    OrderDetail,
    SalesOrder
)

from rest_framework import mixins, response, status, viewsets

from utils.mixins import (
    BaseGenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)

from app.urls import router


class OrderViewset(ListModelMixin,
                   CreateModelMixin,
                   UpdateModelMixin,
                   viewsets.GenericViewSet,
                   BaseGenericViewSet):

    serializer_class = serializers.OrderSerializer
    list_serializer_class = serializers.OrderSerializer
    create_serializer_class = serializers.CreateOrderSerializer
    update_serializer_class = serializers.CreateOrderSerializer

    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):

        try:
            item_order = Item.objects.get(item_id=request.data['item_id'])
        except Item.DoesNotExist:
            return response.Response(
                data={
                    "item_id": "Item Id Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        order_detail_serializer = serializers.CreateOrderDetailSerializer(
            data=request.data
        )

        order_detail_serializer.is_valid(raise_exception=True)

        order_serializer = self.get_serializer(
            data=request.data,
            action='create'
        )

        order_serializer.is_valid(raise_exception=True)

        try:
            order = Order.objects.create(
                obsOrder=order_serializer.data['obsOrder'],
                fechaOrden=order_serializer.data['fechaOrden'],
                fechaSolicitada=order_serializer.data['fechaSolicitada']
            )

            order.ordenCompra = order.id
            order.save()

            sales_order = SalesOrder.objects.create(
                status="inProgress",
                order=order
            )

            sales_order.save()

            cantidad = order_detail_serializer.data['cantidad']
            price = cantidad * item_order.standar_cost

            order_detail = OrderDetail.objects.create(
                cantidad=cantidad,
                udvta=item_order.udVta,
                item=item_order,
                precio=price,
                order=order
            )

            order_detail.save()

            authorization = Authorization.objects.create(
                order=order
            )

            authorization.save()

            order_serializer = serializers.OrderSerializer(order)
        except Exception:
            if "order" in locals():
                order.detele()

            if "sales_order" in locals():
                sales_order.detele()

            if "order_detail" in locals():
                order_detail.detele()

            if "authorization" in locals():
                authorization.detele()

            return response.Response(
                data={
                    "error": "An error ocurre while creating order"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response.Response(
            data=order_serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderDetailViewset(RetrieveModelMixin,
                         UpdateModelMixin,
                         viewsets.GenericViewSet,
                         BaseGenericViewSet):

    serializer_class = serializers.OrderDetail
    retrieve_serializer_class = serializers.OrderDetailSerializer
    update_serializer_class = serializers.UpdateOrderDetailSerializer

    queryset = OrderDetail.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'order': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class AreaStatusViewset(mixins.RetrieveModelMixin,
                        UpdateModelMixin,
                        viewsets.GenericViewSet,
                        BaseGenericViewSet):
    serializer_class = serializers.AuthorizationSerializer
    update_serializer_class = serializers.AuthorizationSerializer
    # Missing filter with Orders that has salesOrder or inProgress
    queryset = Authorization.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'order': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class DeliveredQuantityViewset(ListModelMixin,
                               CreateModelMixin,
                               RetrieveModelMixin,
                               UpdateModelMixin,
                               DestroyModelMixin,
                               viewsets.GenericViewSet,
                               BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.DeliveredQuantitySerializer
    list_serializer_class = serializers.CustomDeliveredQuantitySerializer
    create_serializer_class = serializers.CustomDeliveredQuantitySerializer
    retrieve_serializer_class = serializers.CustomDeliveredQuantitySerializer
    update_serializer_class = serializers.CustomDeliveredQuantitySerializer

    queryset = DeliveredQuantity.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'order': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class InvoiceViewset(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.InvoiceSerializer
    list_serializer_class = serializers.CustomInvoiceSerializer
    create_serializer_class = serializers.CustomInvoiceSerializer
    retrieve_serializer_class = serializers.CustomInvoiceSerializer
    update_serializer_class = serializers.CustomInvoiceSerializer

    queryset = Invoice.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {'invoice_number': self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class DeliverAddressViewset(ListModelMixin,
                            CreateModelMixin,
                            RetrieveModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin,
                            viewsets.GenericViewSet,
                            BaseGenericViewSet):
    "Manage Price Lists"

    serializer_class = serializers.DeliverAddressSerializer
    list_serializer_class = serializers.RetrieveDeliverAddressSerializer
    create_serializer_class = serializers.CustomDeliverAddressSerializer
    retrieve_serializer_class = serializers.RetrieveDeliverAddressSerializer
    update_serializer_class = serializers.CustomDeliverAddressSerializer

    queryset = DeliverAddress.objects.filter(is_active=True)


router.register(
    r'orders',
    OrderViewset,
    basename='order'
)


router.register(
    r'orders-detail',
    OrderDetailViewset,
    basename='orders-detail'
)


router.register(
    r'order-status',
    AreaStatusViewset,
    basename='auth-order'
)

router.register(
    r'delivered-quantities',
    DeliveredQuantityViewset,
    basename='delivered-quantity'
)

router.register(
    r'invoices',
    InvoiceViewset,
    'invoice'
)

router.register(
    r'deliver-addresses',
    DeliverAddressViewset,
    basename='deliver-address'
)
