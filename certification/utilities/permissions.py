#------permission are classified into three types------->
#first-level:-Admin,Superadmin,Superuser (this is  user model class which can be considered as ObjectA)
#second-level:-object 'B' is assigned to user(i.e in object B , ObjectA is assigned), where user called as ObjectA
#third-level:-object 'C' is assigned to object object B(i.e object B is assigned in object C)

#model ObjectB->user field
#model ObjectC->objectB field(objectB id)


#as example, we can consider as , user,company,job where user is ObjectA,company is ObjectB,job is ObjectC

from rest_framework.permissions import BasePermission

CERTIFICATION_PERMISSIONS = {
    "add": "add_certification",
    "change": "change_certification",
    "delete": "delete_certification",
    "view": "view_certification",
    "manage": "manage_certification",
}

def HasPermission(request, codename):
    """Check if the user has a specific Django permission"""
    return request.user.has_perm(f"app_name.{codename}")

def CanManage(request):
    """Check if the user has full manage access"""
    return HasPermission(request, CERTIFICATION_PERMISSIONS["manage"])

class certificationPermission(BasePermission):
    """
    Permission class for managing certifications based strictly on Django permissions.
    """

    def has_permission(self, request, view):
        if CanManage(request):  # If user has manage permission, grant full access
            return True

        if view.action in ["list"]:
            return True

        elif view.action in ["retrieve"]:
            return True

        elif view.action in ["create"]:
            return HasPermission(request, CERTIFICATION_PERMISSIONS["add"])

        elif view.action in ["update", "partial_update"]:
            return HasPermission(request, CERTIFICATION_PERMISSIONS["change"])

        elif view.action == "destroy":
            return HasPermission(request, CERTIFICATION_PERMISSIONS["delete"])

        return False  # Default deny access
