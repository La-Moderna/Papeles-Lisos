from django.contrib import admin

from inventories.models import Item


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


admin.site.register(Item, ItemAdmin)
