from django.contrib import admin


from inventories.models import Inventory
from inventories.models import Item
from inventories.models import Warehouse


class WarehouseAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'description',
    ]


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = [
        'id',
        'description',
        'udVta',
        'access_key',
        'standard_cost',
        'company',
        'is_active'
    ]


class InventoryAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'warehouse',
        'stock',
        'is_active'
    ]


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Item, ItemAdmin)
