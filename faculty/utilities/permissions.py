from rest_framework.permissions import BasePermission

FACULTY_PERMISSIONS = {
    "add": "add_faculty",
    "change": "change_faculty",
    "delete": "delete_faculty",
    "view": "view_faculty",
    "manage": "manage_faculty",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, FACULTY_PERMISSIONS["manage"])

class facultyPermission(BasePermission):
    """
    Permission class for managing faculties based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, FACULTY_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, FACULTY_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, FACULTY_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, FACULTY_PERMISSIONS["delete"])

        return False  # Default deny access
