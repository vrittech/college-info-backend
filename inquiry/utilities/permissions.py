from rest_framework.permissions import BasePermission

INQUIRY_PERMISSIONS = {
    "add": "add_inquiry",
    "change": "change_inquiry",
    "delete": "delete_inquiry",
    "view": "view_inquiry",
    "manage": "manage_inquiry",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, INQUIRY_PERMISSIONS["manage"])

class inquiryPermission(BasePermission):
    """
    Permission class for managing inquiries based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, INQUIRY_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, INQUIRY_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, INQUIRY_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, INQUIRY_PERMISSIONS["delete"])

        return False  # Default deny access
