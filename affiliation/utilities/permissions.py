from rest_framework.permissions import BasePermission

SUPER_ADMIN = 1
ADMIN = 2

AFFILIATION_PERMISSIONS = {
    "add": "add_affiliation",
    "change": "change_affiliation",
    "delete": "delete_affiliation",
    "view": "view_affiliation",
    "manage": "manage_affiliation",
}

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, AFFILIATION_PERMISSIONS["manage"])

class affiliationPermission(BasePermission):
    """
    Permission class for managing affiliations based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
           return True

        elif view.action in ["create"]:
            return HasPermission(request, AFFILIATION_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, AFFILIATION_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, AFFILIATION_PERMISSIONS["delete"])

        return False  # Default deny access
