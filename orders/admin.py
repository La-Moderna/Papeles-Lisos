from django.contrib import admin

from orders.models import Authorization


class AuthorizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'vta', 'cst', 'pln', 'ing',
                    'cxc', 'suaje', 'grabado']


admin.site.register(Authorization, AuthorizationAdmin)
