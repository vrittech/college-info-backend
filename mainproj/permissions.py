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

class DynamicModelPermission(BasePermission):
    """
    Fully dynamic permission class that:
    - Uses only group-based permissions.
    - Prevents users from accessing models they don't have permission for.
    - Allows `list` and `retrieve` for all models except restricted ones.
    - Prevents unauthorized `create`, `update`, and `delete` actions.
    - Prevents users from deleting models in RESTRICTED_DELETE_MODELS (except superusers).
    - Prevents users from deleting their own account.
    """

    def has_permission(self, request, view):
        model_name = getattr(view.queryset.model, "__name__", "").lower()
        group_permissions = get_group_permissions(request.user)

        # Allow `list` and `retrieve` for all models except restricted ones
        if view.action in ["list", "retrieve"] and model_name not in RESTRICTED_PUBLIC_MODELS:
            return True

        # Superusers always have full access
        if request.user.is_superuser:
            return True

        #  Strictly check if the user has permission for this model from groups
        if model_name not in group_permissions:
            return False  # User's groups have NO permission for this model

        # Enforce permission mapping (prevent unauthorized actions)
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            return False  # User's group does NOT have the required permission

        # Prevent deletion of restricted models (except for superusers)
        if view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return request.user.is_superuser

        return True  # Allow access if all checks pass

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission handling.
        """
        model_name = obj.__class__.__name__.lower()
        group_permissions = get_group_permissions(request.user)
        
        if view.action in ["list", "retrieve"]:
            return True

        # Superusers always have full access
        if request.user.is_superuser:
            return True
        
        # Prevent deletion of restricted models (except for superusers)
        if view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return request.user.is_superuser

        # Prevent users from deleting their own account
        if view.action == "destroy" and model_name == "customuser" and obj.id == request.user.id:
            return False

        # Users can only update their own profile
        if view.action in ["update", "partial_update"] and model_name == "customuser":
            return obj.id == request.user.id or request.user.is_staff

        # Strictly check if the user's groups have permission for this model
        if model_name not in group_permissions:
            return False  # User's groups have NO permission for this model

        # Enforce permission mapping at object level
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            return False  # User's groups do NOT have the required permission

        return True  # Allow access if all checks pass
