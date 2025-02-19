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
RESTRICTED_PUBLIC_MODELS = [ "adminlog", "sessions"]

# Models that cannot be deleted except by superusers
RESTRICTED_DELETE_MODELS = ["user", "adminlog", "sessions"]

# Models that college admins can only view (not edit/update)
COLLEGE_ADMIN_VIEW_ONLY_MODELS = ["inquiry", "information"]

# Models that can be publicly listed, retrieved, and written but NOT deleted
RESTRICTED_WRITE_MODELS = ["college"]

# Models that can only be written but NOT publicly listed or retrieved
WRITE_ONLY_MODELS = ["user", "contact", "inquiry"]

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
    Fully dynamic permission class with refined access control:
    - Uses only group-based permissions.
    - Restricts college admins to their assigned college data.
    - Prevents unauthorized `create`, `update`, and `delete` actions.
    - Prevents users from deleting restricted models (except superusers).
    - Prevents users from deleting their own account.
    - Allows specific models to be publicly written but NOT deleted.
    - Restricts specific models to write-only access.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action on the model.
        """
        model_name = getattr(view.queryset.model, "__name__", "").lower()
        if not model_name:
            logger.warning(f"Unable to determine model name for view: {view}")
            return False

        # Restrict public listing and retrieval for certain models
        if view.action in ["list", "retrieve"]:
            if model_name in RESTRICTED_PUBLIC_MODELS or model_name in WRITE_ONLY_MODELS:
                return False
            return True

        # Superusers always have full access (except deleting their own account)
        if request.user.is_superuser:
            return True

        # Restrict college admins from editing/updating certain models
        if hasattr(request.user, "college") and request.user.college:
            if model_name in COLLEGE_ADMIN_VIEW_ONLY_MODELS:
                return view.action in ["list", "retrieve"]

        # Prevent deletion of restricted write models
        if view.action == "destroy" and model_name in RESTRICTED_WRITE_MODELS:
            return False

        # Fetch group permissions for the user
        group_permissions = get_group_permissions(request.user)
        if model_name not in group_permissions:
            logger.warning(f"User {request.user.id} has no permissions for model: {model_name}")
            return False

        # Enforce permission mapping
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            logger.warning(f"User {request.user.id} lacks required permission: {required_permission} for model: {model_name}")
            return False

        return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the object.
        """
        model_name = obj.__class__.__name__.lower()

        # Restrict public listing and retrieval for write-only models
        if view.action in ["list", "retrieve"] and model_name in WRITE_ONLY_MODELS:
            return False

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

        # Prevent deletion of restricted write models
        if view.action == "destroy" and model_name in RESTRICTED_WRITE_MODELS:
            return False

        # Restrict college admins to their own college
        if hasattr(request.user, "college") and request.user.college:
            if hasattr(obj, "college") and obj.college != request.user.college:
                return False
            if model_name in COLLEGE_ADMIN_VIEW_ONLY_MODELS:
                return view.action in ["list", "retrieve"]

        # Fetch group permissions for the user
        group_permissions = get_group_permissions(request.user)
        if model_name not in group_permissions:
            logger.warning(f"User {request.user.id} has no permissions for model: {model_name}")
            return False

        # Enforce permission mapping at object level
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            logger.warning(f"User {request.user.id} lacks required permission: {required_permission} for model: {model_name}")
            return False

        return True
