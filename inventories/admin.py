from django.contrib import admin


from inventories.models import Inventory
from inventories.models import Warehouse


class WarehouseAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'description'
    ]


class InventoryAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'warehouse',
        'stock'
    ]


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Inventory, InventoryAdmin)
