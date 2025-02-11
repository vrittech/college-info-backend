from rest_framework.permissions import BasePermission

DISCIPLINE_PERMISSIONS = {
    "add": "add_discipline",
    "change": "change_discipline",
    "delete": "delete_discipline",
    "view": "view_discipline",
    "manage": "manage_discipline",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, DISCIPLINE_PERMISSIONS["manage"])

class disciplinePermission(BasePermission):
    """
    Permission class for managing disciplines based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, DISCIPLINE_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, DISCIPLINE_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, DISCIPLINE_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, DISCIPLINE_PERMISSIONS["delete"])

        return False  # Default deny access
