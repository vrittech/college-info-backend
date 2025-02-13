from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, GroupExtension, Group

class CustomUserAdmin(BaseUserAdmin):
    exclude = ('user_permissions',)

    # Only include fields that are present in the model
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'professional_image', 'position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    
    list_display = ['username', 'email', 'position', 'phone', 'is_active', 'is_staff', 'professional_image', 'avatar']
    search_fields = ['username', 'email', 'full_name']

    def delete_model(self, request, obj):
        # Prevent deleting superusers (including the logged-in admin)
        if obj.is_superuser and obj != request.user:
            raise PermissionDenied("Superusers cannot be deleted.")
        
        # Call the parent delete method to actually delete the user
        super().delete_model(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)

# Register GroupExtension model
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
