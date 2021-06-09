from django.contrib import admin

from orders import models


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


admin.site.register(models.Authorization, AuthorizationAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.SalesOrder, SalesOrderAdmin)
admin.site.register(models.OrderDetail, OrderDetailAdmin)
