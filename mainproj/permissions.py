from rest_framework.permissions import BasePermission
from django.apps import apps  # To fetch all models dynamically

# Define API action to Django permission mapping
ACTION_PERMISSION_MAPPING = {
    "list": "view",  
    "retrieve": "view",
    "create": "add",
    "update": "change",
    "partial_update": "change",
    "destroy": "delete",
}

# Models that should NOT be publicly listed or retrieved
RESTRICTED_PUBLIC_MODELS = ["user", "adminlog", "sessions"]

# Models that cannot be deleted except by superusers
RESTRICTED_DELETE_MODELS = ["user", "adminlog", "sessions"]

foreign_owner_field = ['user', 'college']
foreign_owner_second_layer = ['college']

# Fetch all registered models dynamically
ALL_MODELS = {model.__name__.lower(): model for model in apps.get_models()}

def get_group_permissions(user):
    """
    Fetch all permissions from user groups.
    Returns a dictionary mapping models to their allowed actions.
    """
    group_permissions = {}

    # Loop through all user groups and collect permissions
    for group in user.groups.all():
        for perm in group.permissions.all():
            # Extract model name and action type from permission codename
            try:
                action, model_name = perm.codename.split("_", 1)  # Example: "add_socialmedia"
                if model_name not in group_permissions:
                    group_permissions[model_name] = set()
                group_permissions[model_name].add(action)
            except ValueError:
                continue  # Skip invalid permissions
    return group_permissions


safe_method = ['list', 'retrieve']

class DynamicModelPermission(BasePermission):
    """
    Fully dynamic permission class that:
    - Uses only group-based permissions.
    - Prevents users from accessing models they don't have permission for.
    - Allows `list` and `retrieve` for all models except restricted ones.
    - Prevents unauthorized `create`, `update`, and `delete` actions.
    - Prevents users from deleting models in RESTRICTED_DELETE_MODELS (except superusers).
    - Prevents users from deleting their own account.
    - Handles multi-level foreign key ownership checks.
    """

    def has_permission(self, request, view):
 
        # Fast track for superusers
        if request.user.is_superuser:
            return True
            
        model_name = getattr(view.queryset.model, "__name__", "").lower()
        group_permissions = get_group_permissions(request.user)
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        
        # Allow `list` and `retrieve` for all models except restricted ones
        if view.action in safe_method and model_name not in RESTRICTED_PUBLIC_MODELS:
            return True

        #  Strictly check if the user has permission for this model from groups
        elif model_name not in group_permissions:
            return False  # User's groups have NO permission for this model

        # Enforce permission mapping (prevent unauthorized actions)
        elif required_permission and required_permission not in group_permissions[model_name]:
            return False  # User's group does NOT have the required permission

        # Prevent deletion of restricted models (except for superusers)
        elif view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return request.user.is_superuser
            
        return True  # If we've reached here, the permission is granted

    def has_object_permission(self, request, view, obj):
  
        """
        Object-level permission handling with multi-level ownership check.
        """
        # Fast track for superusers
        if request.user.is_superuser:
            return True
            
        model_name = obj.__class__.__name__.lower()
        group_permissions = get_group_permissions(request.user)
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        
        # Allow safe methods regardless of ownership
        if view.action in safe_method:
            return True       

        # Strictly check if the user's groups have permission for this model
        if model_name not in group_permissions:
            return False  # User's groups have NO permission for this model

        # Enforce permission mapping at object level
        if required_permission and required_permission in group_permissions[model_name]:
            # First layer ownership check
            for field in foreign_owner_field:
                if hasattr(obj, field):
                    field_value = getattr(obj, field)
                    
                    # Direct user ownership
                    if field == 'user' and field_value == request.user:
                        return True
                    
                    # Second layer ownership check (for fields like 'college')
                    if field in foreign_owner_second_layer:
                        # Get the related object (e.g., college)
                        related_obj = field_value
                        if related_obj:
                            # Check if the user is associated with this object
                            # For example, if college has a 'user' field
                            if hasattr(related_obj, 'user'):
                                return getattr(related_obj, 'user') == request.user
                            
                            # # Or if college has a ManyToMany relationship with users
                            # if hasattr(related_obj, 'users') and hasattr(related_obj.users, 'all'):
                            #     return request.user in related_obj.users.all()
                
            # If we reach here, the object doesn't have any of the expected ownership fields
            # or the user doesn't own the object
            return False
        
        return False  # Default deny if no condition is met