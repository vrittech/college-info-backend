from rest_framework.permissions import BasePermission

EVENT_PERMISSIONS = {
    "add": "add_event",
    "change": "change_event",
    "delete": "delete_event",
    "view": "view_event",
    "manage": "manage_event",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, EVENT_PERMISSIONS["manage"])

class eventPermission(BasePermission):
    """
    Permission class for managing events based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, EVENT_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, EVENT_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, EVENT_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, EVENT_PERMISSIONS["delete"])

        return False  # Default deny access
