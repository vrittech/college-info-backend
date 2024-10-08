from django.contrib.auth.models import Group, Permission
from django.contrib import admin

from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # list_display = ['role',] # this display in outer list form
    exclude = ('user_permissions',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email','avatar','department','position')}),
        ('Permissions', {'fields': ('is_active','is_staff', 'is_superuser','groups')}),
        # ('Social sites',{'fields':('facebook','twitter','tiktok','instagram','youtube')})
        # Add your custom fields here
    )
    pass
    # Your custom admin configurations

admin.site.register(CustomUser, UserAdmin)

admin.site.register(Permission)



