from django.contrib import admin


from inventories.models import Inventory, Item, Warehouse


class WarehouseAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'description',
    ]


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'description',
        'udVta',
        'access_key',
        'standar_cost',
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
