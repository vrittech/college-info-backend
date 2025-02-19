from rest_framework.permissions import BasePermission

CONTACT_PERMISSIONS = {
    "add": "add_contact",
    "change": "change_contact",
    "delete": "delete_contact",
    "view": "view_contact",
    "manage": "manage_contact",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, CONTACT_PERMISSIONS["manage"])

class contactPermission(BasePermission):
    """
    Permission class for managing contacts based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return True

        elif view.action in ["create"]:
            return True

        elif view.action in ["update", "partial_update"]:
            return True

        elif view.action == "destroy":
            return HasPermission(request, CONTACT_PERMISSIONS["delete"])

        return False  # Default deny access
