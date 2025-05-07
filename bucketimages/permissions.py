from rest_framework import permissions

class ViewOnlyOrSuperuserDelete(permissions.BasePermission):
    """
    Allows authenticated users to view data, but only superusers can delete.
    """
    def has_permission(self, request, view):
        # Allow all authenticated users for GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # For DELETE requests, only allow superusers
        if request.method == 'DELETE':
            return request.user and request.user.is_superuser
        
        # Allow POST requests (upload) for authenticated users by default
        # Modify this if you want different behavior for POST
        return request.user and request.user.is_authenticated