from rest_framework.permissions import BasePermission
from django.apps import apps
from django.core.cache import cache
import logging

# Configure logging
logger = logging.getLogger(__name__)

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

# Models that college admins can only view (not edit/update)
COLLEGE_ADMIN_VIEW_ONLY_MODELS = ["inquiry", "informationmanagement"]

# Fetch all registered models dynamically
ALL_MODELS = {model.__name__.lower(): model for model in apps.get_models()}

def get_group_permissions(user):
    """
    Fetch all permissions from user groups.
    Returns a dictionary mapping models to their allowed actions.
    """
    cache_key = f"user_{user.id}_group_permissions"
    group_permissions = cache.get(cache_key)

    if group_permissions is None:
        group_permissions = {}
        for group in user.groups.all():
            for perm in group.permissions.all():
                try:
                    action, model_name = perm.codename.split("_", 1)  # Example: "add_socialmedia"
                    if model_name not in group_permissions:
                        group_permissions[model_name] = set()
                    group_permissions[model_name].add(action)
                except ValueError:
                    logger.warning(f"Invalid permission codename: {perm.codename}")
                    continue  # Skip invalid permissions

        cache.set(cache_key, group_permissions, timeout=60)  # Cache for 60 seconds

    return group_permissions

class DynamicModelPermission(BasePermission):
    """
    Fully dynamic permission class that:
    - Uses only group-based permissions.
    - Restricts college admins to their assigned college data.
    - Prevents unauthorized `create`, `update`, and `delete` actions.
    - Prevents users from deleting restricted models (except superusers).
    - Prevents users from deleting their own account.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action on the model.
        """
        # Get the model name from the view's queryset
        model_name = getattr(view.queryset.model, "__name__", "").lower()
        if not model_name:
            logger.warning(f"Unable to determine model name for view: {view}")
            return False  # Deny access if the model name cannot be determined

        # Allow `list` and `retrieve` for all models except restricted ones
        if view.action in ["list", "retrieve"]:
            if model_name in RESTRICTED_PUBLIC_MODELS:
                return False  # Deny access to restricted models
            return True  # Allow access to non-restricted models

        # Superusers always have full access (except deleting their own account)
        if request.user.is_superuser:
            return True

        # Restrict college admins from editing/updating certain models
        if hasattr(request.user, "college") and request.user.college:
            if model_name in COLLEGE_ADMIN_VIEW_ONLY_MODELS:
                return view.action in ["list", "retrieve"]  # College admin can only view these models

        # Fetch group permissions for the user
        group_permissions = get_group_permissions(request.user)

        # Deny access if the user's groups have NO permission for this model
        if model_name not in group_permissions:
            logger.warning(f"User {request.user.id} has no permissions for model: {model_name}")
            return False

        # Enforce permission mapping (prevent unauthorized actions)
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            logger.warning(f"User {request.user.id} lacks required permission: {required_permission} for model: {model_name}")
            return False  # User's group does NOT have the required permission

        # Prevent deletion of restricted models (except for superusers)
        if view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return request.user.is_superuser

        return True  # Allow access if all checks pass

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the object.
        """
        model_name = obj.__class__.__name__.lower()

        # Allow listing and retrieving objects
        if view.action in ["list", "retrieve"]:
            return True

        # Superusers always have full access (except deleting their own account)
        if request.user.is_superuser:
            if view.action == "destroy" and model_name == "customuser" and obj.id == request.user.id:
                return False  # Prevent superusers from deleting their own account
            return True

        # Prevent users from deleting their own account
        if view.action == "destroy" and model_name == "customuser" and obj.id == request.user.id:
            return False

        # Prevent deletion of restricted models (except for superusers)
        if view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return False

        # Restrict college admins to their own college
        if hasattr(request.user, "college") and request.user.college:
            if hasattr(obj, "college") and obj.college != request.user.college:
                return False  # Deny access if the object does not belong to the user's college

            # Restrict college admins from editing certain models
            if model_name in COLLEGE_ADMIN_VIEW_ONLY_MODELS:
                return view.action in ["list", "retrieve"]  # Only allow viewing

        # Fetch group permissions for the user
        group_permissions = get_group_permissions(request.user)

        # Deny access if the user's groups have NO permission for this model
        if model_name not in group_permissions:
            logger.warning(f"User {request.user.id} has no permissions for model: {model_name}")
            return False

        # Enforce permission mapping at object level
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            logger.warning(f"User {request.user.id} lacks required permission: {required_permission} for model: {model_name}")
            return False  # User's groups do NOT have the required permission

        return True  # Allow access if all checks pass