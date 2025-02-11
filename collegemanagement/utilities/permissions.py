from rest_framework.permissions import BasePermission

COLLEGE_MANAGEMENT_PERMISSIONS = {
    "add": "add_college",
    "change": "change_college",
    "delete": "delete_college",
    "view": "view_college",
    "manage": "manage_college",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["manage"])

class collegemanagementPermission(BasePermission):
    """
    Permission class for managing college data strictly based on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True
        
        elif view.action in ["retrieve"]:
            return True

        elif view.action in ["create"]:
            return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["delete"])

        return False  # Default deny access
