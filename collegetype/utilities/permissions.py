from rest_framework.permissions import BasePermission

COLLEGE_TYPE_PERMISSIONS = {
    "add": "add_collegetype",
    "change": "change_collegetype",
    "delete": "delete_collegetype",
    "view": "view_collegetype",
    "manage": "manage_college_type",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, COLLEGE_TYPE_PERMISSIONS["manage"])

class collegetypePermission(BasePermission):
    """
    Permission class for managing college types based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
           return True

        elif view.action in ["retrieve"]:
            return True

        elif view.action in ["create"]:
            return HasPermission(request, COLLEGE_TYPE_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, COLLEGE_TYPE_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, COLLEGE_TYPE_PERMISSIONS["delete"])

        return False  # Default deny access
