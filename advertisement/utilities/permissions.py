from rest_framework.permissions import BasePermission

SUPER_ADMIN = 1
ADMIN = 2

ADVERTISEMENT_PERMISSIONS = {
    "add": "add_advertisement",
    "change": "change_advertisement",
    "delete": "delete_advertisement",
    "view": "view_advertisement",
    "manage": "manage_advertisement",
}

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def SuperAdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.is_superuser)

def AdminLevel(request):
    return bool(IsAuthenticated(request) and request.user.role in [ADMIN, SUPER_ADMIN])

def HasPermission(request, codename):
    """Check if the user has a specific permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, ADVERTISEMENT_PERMISSIONS["manage"])

def isOwner(request, obj=None):
    """Check if the request user is the owner of the object"""
    if obj:
        return obj.user_id == request.user.id
    return str(request.user.id) == str(request.data.get("user")) or (not request.data and not request.POST)

class advertisementPermission(BasePermission):
    """
    Permission class for managing advertisements based on user permissions and ownership.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If the user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return True

        elif view.action in ["create"]:
            return HasPermission(request, ADVERTISEMENT_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            obj = view.get_object()
            return (HasPermission(request, ADVERTISEMENT_PERMISSIONS["change"]))

        elif view.action == "destroy":
            obj = view.get_object()
            return (HasPermission(request, ADVERTISEMENT_PERMISSIONS["delete"]))

        return False  # Default deny access
