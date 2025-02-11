from rest_framework.permissions import BasePermission

SUPER_ADMIN_DETAILS_PERMISSIONS = {
    "add": "add_superadmindetails",
    "change": "change_superadmindetails",
    "delete": "delete_superadmindetails",
    "view": "view_superadmindetails",
    "manage": "manage_super_admin_details",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, SUPER_ADMIN_DETAILS_PERMISSIONS["manage"])

class superadmindetailsPermission(BasePermission):
    """
    Permission class for managing super admin details based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, SUPER_ADMIN_DETAILS_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, SUPER_ADMIN_DETAILS_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, SUPER_ADMIN_DETAILS_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, SUPER_ADMIN_DETAILS_PERMISSIONS["delete"])

        return False  # Default deny access
