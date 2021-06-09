from django.contrib import admin

from orders.models import (
    Authorization,
    DeliverAddress,
    DeliveredQuantity,
    Invoice,
    Order,
    OrderDetail,
    SalesOrder
)


class AuthorizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'vta', 'cst', 'pln', 'ing',
                    'cxc', 'suaje', 'grabado']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'obsOrder', 'ordenCompra',
                    'fechaOrden', 'fechaSolicitada']


class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'order']


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'cantidad', 'udvta',
                    'precio', 'item']


class DeliverAddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'client',
        'del_address',
        'is_active'
    ]


class DeliveredQuantityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'order',
        'reg_type',
        'quantity',
        'item',
        'is_active'
    ]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'invoice_number',
        'item',
        'invoice_date',
        'client',
        'is_active'
    ]


admin.site.register(Authorization, AuthorizationAdmin)
admin.site.register(DeliverAddress, DeliverAddressAdmin)
admin.site.register(DeliveredQuantity, DeliveredQuantityAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(SalesOrder, SalesOrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
