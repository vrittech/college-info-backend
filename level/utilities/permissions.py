from rest_framework.permissions import BasePermission

LEVEL_PERMISSIONS = {
    "add": "add_level",
    "change": "change_level",
    "delete": "delete_level",
    "view": "view_level",
    "manage": "manage_level",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, LEVEL_PERMISSIONS["manage"])

class levelPermission(BasePermission):
    """
    Permission class for managing levels based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, LEVEL_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, LEVEL_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, LEVEL_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, LEVEL_PERMISSIONS["delete"])

        return False  # Default deny access
