from rest_framework.permissions import BasePermission

DURATION_PERMISSIONS = {
    "add": "add_duration",
    "change": "change_duration",
    "delete": "delete_duration",
    "view": "view_duration",
    "manage": "manage_duration",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, DURATION_PERMISSIONS["manage"])

class durationPermission(BasePermission):
    """
    Permission class for managing durations based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True
        
        elif view.action in ["retrieve"]:
            return HasPermission(request, DURATION_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, DURATION_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, DURATION_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, DURATION_PERMISSIONS["delete"])

        return False  # Default deny access
