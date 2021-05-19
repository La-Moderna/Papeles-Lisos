from django.contrib import admin

from inventories.models import Item


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


admin.site.register(Item, ItemAdmin)
