from rest_framework.permissions import BasePermission

REQUEST_SUBMISSION_PERMISSIONS = {
    "add": "add_requestsubmission",
    "change": "change_requestsubmission",
    "delete": "delete_requestsubmission",
    "view": "view_requestsubmission",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

class requestsubmissionPermission(BasePermission):
    """
    Permission class for managing request submissions based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return HasPermission(request, REQUEST_SUBMISSION_PERMISSIONS["view"])

        elif view.action in ["create"]:
            return HasPermission(request, REQUEST_SUBMISSION_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, REQUEST_SUBMISSION_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, REQUEST_SUBMISSION_PERMISSIONS["delete"])

        return False  # Default deny access
