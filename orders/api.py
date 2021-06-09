from django.shortcuts import get_object_or_404

from inventories.models import Item

from orders import models, serializers

from rest_framework import response, status, viewsets

from utils.mixins import (
    BaseGenericViewSet,
    CreateModelMixin,
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
    queryset = models.Order.objects.all()
    create_serializer_class = serializers.CreateOrderSerializer
    list_serializer_class = serializers.OrderSerializer
    update_serializer_class = serializers.CreateOrderSerializer

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

        if (not order_detail_serializer.is_valid()):
            return response.Response(
                data=order_detail_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        order_serializer = serializers.CreateOrderSerializer(
            data=request.data
        )

        if order_serializer.is_valid():
            order = models.Order.objects.create()
            order.ordenCompra = order.id
            order.obsOrder = order_serializer.data['obsOrder']
            order.fechaOrden = order_serializer.data['fechaOrden']
            order.fechaSolicitada = order_serializer.data['fechaSolicitada']
            order.save()

            sales_order = models.SalesOrder.objects.create(
                status="inProgress",
                order=order
            )

            sales_order.save()

            cantidad = order_detail_serializer.data['cantidad']
            price = cantidad * item_order.standar_cost

            order_detail = models.OrderDetail.objects.create(
                cantidad=cantidad,
                udvta=item_order.udVta,
                item=item_order,
                precio=price,
                order=order
            )

            order_detail.save()

            authorization = models.Authorization.objects.create(
                order=order
            )

            authorization.save()

        else:
            return response.Response(
                data=order_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        order_serializer = serializers.OrderSerializer(order)

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

    queryset = models.OrderDetail.objects.all()

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


class AreaStatusViewset(RetrieveModelMixin,
                        viewsets.GenericViewSet,
                        BaseGenericViewSet):
    serializer_class = serializers.AuthorizationSerializer
    retrieve_serializer_class = serializers.AuthorizationSerializer

    # Missing filter with Orders that has salesOrder or inProgress
    queryset = models.Authorization.objects.all()

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

    # Missing check if user has rol of VTA or AGE
    # Missing order filter (all, in progress, processed)
    def list(self, request, *args, **kwargs):
        return super(AreaStatusViewset, self).list(request, *args, **kwargs)


router.register(
    r'order',
    OrderViewset,
    'order'
)


router.register(
    r'order/detail',
    OrderDetailViewset,
    'order-detail'
)


router.register(
    r'order/status',
    AreaStatusViewset,
    'auth-order'
)
