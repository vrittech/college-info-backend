from rest_framework.permissions import BasePermission

SOCIAL_MEDIA_PERMISSIONS = {
    "add": "add_socialmedia",
    "change": "change_socialmedia",
    "delete": "delete_socialmedia",
    "view": "view_socialmedia",
    "manage": "manage_social_media",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, SOCIAL_MEDIA_PERMISSIONS["manage"])

class socialmediaPermission(BasePermission):
    """
    Permission class for managing social media based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True
        
        elif view.action in ["retrieve"]:
            return HasPermission(request, SOCIAL_MEDIA_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, SOCIAL_MEDIA_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, SOCIAL_MEDIA_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, SOCIAL_MEDIA_PERMISSIONS["delete"])

        return False  # Default deny access
