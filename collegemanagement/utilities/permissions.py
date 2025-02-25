from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

COLLEGE_MANAGEMENT_PERMISSIONS = {
    "add": "add_college",
    "change": "change_college",
    "delete": "delete_college",
    "view": "view_college",
    "manage": "manage_college",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["manage"])

class collegemanagementPermission(BasePermission):
    """
    Permission class for managing college data strictly based on Django permissions.
    """
    
    def has_permission(self, request, view):
        # If user is not authenticated, try to authenticate using the access token from the payload.
        if not request.user or not request.user.is_authenticated:
            access_token = request.data.get("accessToken")
            if not access_token:
                print("❌ No access token provided!")
                return False  # Deny access immediately

            jwt_authenticator = JWTAuthentication()
            try:
                validated_token = jwt_authenticator.get_validated_token(access_token)
                user = jwt_authenticator.get_user(validated_token)
                request.user = user  # Assign authenticated user to request
            except Exception as e:
                print(f"❌ JWT Authentication failed: {str(e)}")
                return False  # Deny access

        # Debugging: Check user authentication status
        print("✅ Authenticated user:", request.user)
        print("✅ Is authenticated:", request.user.is_authenticated)

        # Fetch and log user groups
        user_groups = list(request.user.groups.values_list('name', flat=True))
        print("🔍 User groups:", user_groups)

        # Allow if the user is in the "College Admin" group
        if request.user.groups.filter(name="College Admin").exists():
            print("✅ User is in 'College Admin' group")
            return True

        # Otherwise, check if the user has the required permission
        has_permission = request.user.has_perm("collegemanagement.add_college")
        print(f"🔍 User has permission 'collegemanagement.add_college': {has_permission}")

        return has_permission

    # def has_permission(self, request, view):
    #     if CanManage(request):  # If user has manage permission, grant full access
    #         return True

    #     if view.action in ["list"]:
    #         return True
        
    #     elif view.action in ["retrieve"]:
    #         return True

    #     elif view.action in ["create"]:
    #         return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["add"])

    #     elif view.action in ["update", "partial_update"]:
    #         return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["change"])

    #     elif view.action == "destroy":
    #         return HasPermission(request, COLLEGE_MANAGEMENT_PERMISSIONS["delete"])

    #     return False  # Default deny access
