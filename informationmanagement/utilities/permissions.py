from rest_framework.permissions import BasePermission

INFORMATION_MANAGEMENT_PERMISSIONS = {
    "add": "add_information",
    "change": "change_information",
    "delete": "delete_information",
    "view": "view_information",
    "manage": "manage_information",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, INFORMATION_MANAGEMENT_PERMISSIONS["manage"])

class informationmanagementPermission(BasePermission):
    """
    Permission class for managing information based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, INFORMATION_MANAGEMENT_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, INFORMATION_MANAGEMENT_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, INFORMATION_MANAGEMENT_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, INFORMATION_MANAGEMENT_PERMISSIONS["delete"])

        return False  # Default deny access
