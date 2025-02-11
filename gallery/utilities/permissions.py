from rest_framework.permissions import BasePermission

GALLERY_PERMISSIONS = {
    "add": "add_gallery",
    "change": "change_gallery",
    "delete": "delete_gallery",
    "view": "view_gallery",
    "manage": "manage_gallery",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, GALLERY_PERMISSIONS["manage"])

class galleryPermission(BasePermission):
    """
    Permission class for managing galleries based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, GALLERY_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, GALLERY_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, GALLERY_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, GALLERY_PERMISSIONS["delete"])

        return False  # Default deny access
