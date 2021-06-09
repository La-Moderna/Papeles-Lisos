from clients.models import Agent, Balance, Client, PriceList

from django.contrib import admin


class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'representant',
        'company',
        'is_active',
    ]


class BalanceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order_balance',
        'facture_balance',
        'company',
        'is_active',
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'client_id',
        'status',
        'agent',
        'warehouse',
        'is_active'
    ]


class PriceListAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'price_list_id',
        'company',
        'item',
        'discount_level',
        'start_date',
        'end_date',
        'is_active'
    ]


admin.site.register(Agent, AgentAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(PriceList, PriceListAdmin)
