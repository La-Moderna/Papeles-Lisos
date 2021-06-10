from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from users.models import Permission, Role, User


class CustomUserAdmin(UserAdmin):
    """Admin for user"""

    ordering = ['email']
    list_display = ['email', 'name', 'last_name', 'is_active']

    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['email']
    filter_horizontal = ['groups', 'user_permissions', 'roles']
    fieldsets = (
        ('Personal info', {'fields': (
            'email', 'password', 'name', 'last_name'
        )}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups', 'user_permissions', 'roles')
        }),
    )

    add_fieldsets = (
        ('Personal info', {'fields': ('email', 'password1', 'password2')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups', 'user_permissions', 'roles')
        }),
    )


class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]
    filter_horizontal = ['permissions']


class PermissionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'codename',
        'description'
    ]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
