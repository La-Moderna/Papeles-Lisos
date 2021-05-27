from clients.models import Agent
from clients.models import Balance

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


admin.site.register(Agent, AgentAdmin)
admin.site.register(Balance, BalanceAdmin)
