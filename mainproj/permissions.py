from rest_framework.permissions import BasePermission

# Define public access models for specific actions
MAPPING_API = {
    "list": ["blog", "course"],  # Public listing
    "create": ["contact", "user", "inquiry"],  # Public creation
}

# Define models that cannot be deleted except by superusers
RESTRICTED_DELETE_MODELS = ["course", "blog"]

def model_permissions(model_name):
    """
    Fetch permissions dynamically based on model name.
    Standard Django permission structure is used.
    """
    model_name = model_name.lower()
    return {
        "add": f"add_{model_name}",
        "change": f"change_{model_name}",
        "delete": f"delete_{model_name}",
        "view": f"view_{model_name}",
        "manage": f"manage_{model_name}",
        "public": f"public_{model_name}",
        "all": f"all_{model_name}",
    }

class AllPermission(BasePermission):
    """
    A dynamic permission class that:
    - Maps API actions to public models.
    - Uses Django's built-in permissions for restricted models.
    - Prevents users from deleting models in RESTRICTED_DELETE_MODELS (except superusers).
    - Prevents users from deleting their own account.
    - Ensures users can only update their own profiles.
    """

    def has_permission(self, request, view):
        model_name = getattr(view.queryset.model, "__name__", "").lower()
        permissions = model_permissions(model_name)

        # Allow public access if model exists in MAPPING_API for the current action
        if view.action in MAPPING_API and model_name in MAPPING_API[view.action]:
            return True

        # Full access for superusers or staff with 'all_{model}' permission
        if request.user.is_superuser or (request.user.is_staff and request.user.has_perm(permissions["all"])):
            return True

        # Prevent deletion of models in RESTRICTED_DELETE_MODELS (except for superusers)
        if view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return request.user.is_superuser  # Only superusers can delete

        # Prevent unauthenticated users from accessing private models
        if not request.user.is_authenticated and model_name not in MAPPING_API.get(view.action, []):
            return False

        # Standard Django permission checks
        if view.action == "list":
            return request.user.has_perm(permissions["view"])

        elif view.action == "retrieve":
            return request.user.has_perm(permissions["view"])

        elif view.action == "create":
            return request.user.has_perm(permissions["add"])

        elif view.action in ["update", "partial_update"]:
            return request.user.has_perm(permissions["change"])

        elif view.action == "destroy":
            return request.user.has_perm(permissions["delete"])

        return False  # Default deny access

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission handling.
        """
        model_name = obj.__class__.__name__.lower()
        permissions = model_permissions(model_name)

        if request.user.is_superuser or request.user.has_perm(permissions["all"]):
            return True  # Superusers and users with 'all_{model}' permission get full access

        # Prevent deletion of restricted models (except for superusers)
        if view.action == "destroy" and model_name in RESTRICTED_DELETE_MODELS:
            return request.user.is_superuser

        # Prevent users from deleting their own account
        if view.action == "destroy" and model_name == "CustomUser" and obj.id == request.user.id:
            return False  # Users cannot delete themselves

        # Users can only update their own profile
        if view.action in ["update", "partial_update"] and model_name == "CustomUser":
            return obj.id == request.user.id or request.user.is_staff

        # Ensure delete permissions are explicitly granted
        if view.action == "destroy":
            return request.user.has_perm(permissions["delete"])

        return False  # Default deny access
