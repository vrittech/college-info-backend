from rest_framework.permissions import BasePermission

COURSE_MANAGEMENT_PERMISSIONS = {
    "add": "add_course",
    "change": "change_course",
    "delete": "delete_course",
    "view": "view_course",
    "manage": "manage_course",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, COURSE_MANAGEMENT_PERMISSIONS["manage"])

class coursemanagementPermission(BasePermission):
    """
    Permission class for managing courses based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True
        
        elif view.action in ["retrieve"]:
            return True

        elif view.action in ["create"]:
            return HasPermission(request, COURSE_MANAGEMENT_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, COURSE_MANAGEMENT_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, COURSE_MANAGEMENT_PERMISSIONS["delete"])

        return False  # Default deny access
