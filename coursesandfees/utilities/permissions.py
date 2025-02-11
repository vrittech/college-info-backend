from rest_framework.permissions import BasePermission

COURSES_AND_FEES_PERMISSIONS = {
    "add": "add_coursesandfees",
    "change": "change_coursesandfees",
    "delete": "delete_coursesandfees",
    "view": "view_coursesandfees",
    "manage": "manage_courses_and_fees",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, COURSES_AND_FEES_PERMISSIONS["manage"])

class coursesandfeesPermission(BasePermission):
    """
    Permission class for managing courses and fees based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
           return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, COURSES_AND_FEES_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, COURSES_AND_FEES_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, COURSES_AND_FEES_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, COURSES_AND_FEES_PERMISSIONS["delete"])

        return False  # Default deny access
