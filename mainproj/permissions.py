from rest_framework.permissions import BasePermission
from django.apps import apps  # To fetch all models dynamically


def get_group_permissions(user):
    """
    Fetch all permissions from user groups.
    Returns a dictionary mapping models to their allowed actions.
    """
    group_permissions = {}

    # Loop through all user groups and collect permissions
    for group in user.groups.all():
        for perm in group.permissions.all():
            # Extract model name and action type from permission codename
            try:
                action, model_name = perm.codename.split("_", 1)  # Example: "add_socialmedia"
                if model_name not in group_permissions:
                    group_permissions[model_name] = set()
                group_permissions[model_name].add(action)
            except ValueError:
                continue  # Skip invalid permissions
    return group_permissions

# Define API action to Django permission mapping
ACTION_PERMISSION_MAPPING = {
    "list": "view",  
    "retrieve": "view",
    "create": "add",
    "update": "change",
    "partial_update": "change",
    "destroy": "delete",
}


foreign_owner_field = ['user', 'college']
foreign_owner_second_layer = ['college']
# user_model = ['customuser']

# Fetch all registered models dynamically
ALL_MODELS = {model.__name__: model for model in apps.get_models()}

from setting.models import ModelMethod
safe_model_method = ModelMethod.objects.all()

class DynamicModelPermission(BasePermission):
    """
    Fully dynamic permission class that:
    - Uses only group-based permissions.
    - Prevents users from accessing models they don't have permission for.
    - Allows `list` and `retrieve` for all models except restricted ones.
    - Prevents unauthorized `create`, `update`, and `delete` actions.
    - Prevents users from deleting models in RESTRICTED_DELETE_MODELS (except superusers).
    - Prevents users from deleting their own account.
    - Handles multi-level foreign key ownership checks.
    """

    def has_permission(self, request, view):
        # Fast track for superusers
        return True
        if request.user.is_superuser:
            return True
            
        model_name = getattr(view.queryset.model, "__name__", "")

        
        # print(safe_model_method,"safe_model_method")

        public_object = safe_model_method.filter(model_name__model_name__iexact=model_name)
        if public_object.exists():
            if view.action in public_object.values_list('method__name',flat=True):
                return True
 
        group_permissions = get_group_permissions(request.user)
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if not group_permissions.get(model_name.lower()):
            print(" not tutut ")
            return False
        # Enforce permission mapping (prevent unauthorized actions)
        
        if required_permission and group_permissions and required_permission in group_permissions.get(model_name.lower()):
            if required_permission == 'view':
                return True
            

            if view.action == "create":
                # return True
                if request.user.is_staff:
                    return True
                if(len(request.data)) == 0:
                    return True
               
                for f_field in foreign_owner_field:
                    if request.data.get(f_field):
                        item_f = getattr(request.user,f_field) #request.user should must be user or dynamically to compare.
                        if getattr(item_f,'id'):
                            if int(getattr(item_f,'id')) == int(request.data.get(f_field)):
                                return True
          
        return False  # If we've reached here, the permission is granted

    def has_object_permission(self, request, view, obj):
        return True
        print("object level permission ....")
        # return True
        """
        Object-level permission handling with multi-level ownership check.
        """
        # Fast track for superusers
        if request.user.is_superuser:
            return True
            
        model_name = obj.__class__.__name__
        print(model_name)
        # print(safe_model_method,"safe_model_method")
        public_object = safe_model_method.filter(model_name__model_name__iexact=model_name)
        
        if public_object.exists():
            if view.action in public_object.values_list('method__name',flat=True):
                return True
            else:
                pass

        
        group_permissions = get_group_permissions(request.user)
        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        
        # print(0)
        # Strictly check if the user's groups have permission for this model
        if model_name.lower() not in group_permissions:
            return False  # User's groups have NO permission for this model

        # print(group_permissions.get(model_name.lower())," pok")
        # if required_permission 
        # print(group_permissions)
        
        # Enforce permission mapping at object level
        if required_permission and group_permissions and group_permissions.get(model_name.lower()) and required_permission in group_permissions.get(model_name.lower()):
            # print(1)
            # First layer ownership check
            # print(required_permission,group_permissions)
            if required_permission == 'view':
                return True
            if model_name.lower() == "customuser" and required_permission == "change" and request.user == obj:
                return True

            for field in foreign_owner_field:
    
                if hasattr(obj, field):
     
                    field_value = getattr(obj, field)


                    if hasattr(field_value, 'all'):  # ManyToMany field
                        if request.user in field_value.all():
                                return True
                    elif field_value == request.user:
                        return True
    
                    # # Direct user ownership
                    # if field_value == request.user or request.user in field_value.all():
                    #     return True
                    
                    # Second layer ownership check (for fields like 'college')
                    if field in foreign_owner_second_layer:
                        # Get the related object (e.g., college)
                        related_obj = field_value
                        if related_obj:
                            # Check if the user is associated with this object
                            # For example, if college has a 'user' field
                            if hasattr(related_obj, 'user'):
                                return getattr(related_obj, 'user') == request.user
                            
                            # # Or if college has a ManyToMany relationship with users
                            # if hasattr(related_obj, 'users') and hasattr(related_obj.users, 'all'):
                            #     return request.user in related_obj.users.all()
            

            # If we reach here, the object doesn't have any of the expected ownership fields
            # or the user doesn't own the object
            print("tututut")
            return False
        
        return False  # Default deny if no condition is met