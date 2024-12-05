from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, GroupExtension

class CustomUserAdmin(BaseUserAdmin):
    exclude = ('user_permissions',)
    
    # Only include fields that are present in the model
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email','roles','phone', 'avatar', 'professional_image', 'position',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups')}),
    )
    
    list_display = ['username', 'email', 'position','roles','phone', 'is_active', 'is_staff', 'professional_image', 'avatar']
    search_fields = ['username', 'email', 'full_name','roles',]

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(GroupExtension)
class GroupExtensionAdmin(admin.ModelAdmin):
    list_display = ['group', 'position']
    search_fields = ['group__name']
    list_filter = ['position']
    ordering = ['position']

    def save_model(self, request, obj, form, change):
        # Override save_model to handle custom position saving logic if needed
        super().save_model(request, obj, form, change)

# Unregister and register Group to customize admin panel if necessary
admin.site.unregister(Group)
admin.site.register(Group)
