from django.contrib import admin


from inventories.models import Inventory, Item, Warehouse


class WarehouseAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name'
    ]


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['item_id']
    list_display = [
        'id',
        'item_id',
        'description',
        'udVta',
        'access_key',
        'standard_cost',
        'company',
        'is_active'
    ]


class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['item__item_id']
    list_display = [
        'id',
        'warehouse',
        'item',
        'stock',
        'is_active'
    ]


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Item, ItemAdmin)
