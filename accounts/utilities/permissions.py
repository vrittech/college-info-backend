# #------permission are classified into three types------->
# #first-level:-Admin,Superadmin,Superuser (this is  user model class which can be considered as ObjectA)
# #second-level:-object 'B' is assigned to user(i.e in object B , ObjectA is assigned), where user called as ObjectA
# #third-level:-object 'C' is assigned to object object B(i.e object B is assigned in object C)

# #model ObjectB->user field
# #model ObjectC->objectB field(objectB id)


# #as example, we can consider as , user,company,job where user is ObjectA,company is ObjectB,job is ObjectC

# from rest_framework.permissions import BasePermission

# SUPER_ADMIN = 1
# ADMIN = 2


# def IsAuthenticated(request):
#     return bool(request.user and request.user.is_authenticated)

# def SuperAdminLevel(request):
#     return bool(IsAuthenticated(request) and request.user.is_superuser)

# def AdminLevel(request):
#     return bool(IsAuthenticated(request) and request.user.role in [ADMIN,SUPER_ADMIN])

# def isOwner(request):
#     if str(request.user.id) == str(request.data.get('user')):
#         return True
    
#     elif len(request.data)==0 and len(request.POST)==0:
#         return True

#     return False


# # def ObjectBOwner(request):
# #     company = ObjectB.objects.filter(id = request.data.get('objectb'),user = request.user.id)
# #     if company.exists():
# #         return True
# #     return False

# class accountsPermission(BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ["list"]:
#             return True
#         elif view.action in ['retrieve']:
#             return isOwner(request)
#         elif view.action in ['create','update']:
#             return isOwner(request) #second level
#             return ObjectBOwner(request) #third level
#         elif view.action == "partial_update":
#             return view.get_object().user_id == request.user.id
#         elif view.action == 'destroy':
#             return isOwner(request)

from rest_framework.permissions import BasePermission, SAFE_METHODS

ACCOUNTS_PERMISSIONS = {
    "add": "add_customuser",
    "change": "change_customuser",
    "delete": "delete_customuser",
    "view": "view_customuser",
    "verify": "can_verify_user",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def IsSelfOrAdmin(request, obj):
    """Ensure users can only modify their own account unless they have admin privileges"""
    return obj.id == request.user.id or request.user.is_superuser or request.user.is_staff

class accountsPermission(BasePermission):
    """
    Permission class for managing user accounts, ensuring high security.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:  # Superuser has all permissions
            return True

        if view.action in ["list"]:
            return HasPermission(request, ACCOUNTS_PERMISSIONS["view"]) and request.user.is_staff  # Restrict list access to staff/admins

        elif view.action in ["retrieve"]:
            return HasPermission(request, ACCOUNTS_PERMISSIONS["view"]) and (request.user.is_staff or request.user.id == view.kwargs.get('pk'))

        elif view.action in ["create"]:
            return True  # Allow anyone (even unauthenticated users) to sign up

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, ACCOUNTS_PERMISSIONS["change"]) and request.user.is_authenticated  # User must be logged in

        elif view.action == "destroy":
            return HasPermission(request, ACCOUNTS_PERMISSIONS["delete"]) and request.user.is_superuser  # Only superusers can delete accounts

        return False  # Default deny access

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to ensure users can only modify their own account,
        unless they have admin/superuser privileges.
        """
        if request.user.is_superuser:  # Superuser has full access
            return True

        if view.action in SAFE_METHODS:  # Read-only permissions for users
            return HasPermission(request, ACCOUNTS_PERMISSIONS["view"])

        if view.action in ["update", "partial_update"]:
            return HasPermission(request, ACCOUNTS_PERMISSIONS["change"]) and IsSelfOrAdmin(request, obj)

        if view.action == "destroy":
            return HasPermission(request, ACCOUNTS_PERMISSIONS["delete"]) and request.user.is_superuser  # Only superusers can delete

        return False  # Default deny access
