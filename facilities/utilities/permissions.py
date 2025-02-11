from rest_framework.permissions import BasePermission

FACILITIES_PERMISSIONS = {
    "add": "add_facility",
    "change": "change_facility",
    "delete": "delete_facility",
    "view": "view_facility",
    "manage": "manage_facility",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, FACILITIES_PERMISSIONS["manage"])

class facilitiesPermission(BasePermission):
    """
    Permission class for managing facilities based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, FACILITIES_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, FACILITIES_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, FACILITIES_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, FACILITIES_PERMISSIONS["delete"])

        return False  # Default deny access
