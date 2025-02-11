from rest_framework.permissions import BasePermission

DISTRICT_PERMISSIONS = {
    "add": "add_district",
    "change": "change_district",
    "delete": "delete_district",
    "view": "view_district",
    "manage": "manage_district",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, DISTRICT_PERMISSIONS["manage"])

class districtPermission(BasePermission):
    """
    Permission class for managing districts based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, DISTRICT_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, DISTRICT_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, DISTRICT_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, DISTRICT_PERMISSIONS["delete"])

        return False  # Default deny access
