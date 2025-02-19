from rest_framework.permissions import BasePermission
from django.apps import apps
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

# Define API action to Django permission mapping
ACTION_PERMISSION_MAPPING = {
    "list": "view",
    "retrieve": "view",
    "create": "add",
    "update": "change",
    "partial_update": "change",
    "destroy": "delete",
}

# Models that should NOT be publicly listed or retrieved
RESTRICTED_PUBLIC_MODELS = [ "adminlog", "sessions"]

# Models that cannot be deleted except by superusers
RESTRICTED_DELETE_MODELS = ["user", "adminlog", "sessions"]

# Models that college admins can only view (not edit/update)
COLLEGE_ADMIN_VIEW_ONLY_MODELS = ["inquiry", "information"]

# Models that can be publicly listed, retrieved, and written but NOT deleted
RESTRICTED_WRITE_MODELS = ["college"]

# Models that can only be written but NOT publicly listed or retrieved
WRITE_ONLY_MODELS = ["user", "contact", "inquiry"]

# Fetch all registered models dynamically
ALL_MODELS = {model.__name__.lower(): model for model in apps.get_models()}

def get_related_models(model):
    """
    Fetch related models (ManyToMany or ForeignKey) for a given model.
    """
    related_models = set()
    if model:
        for field in model._meta.get_fields():
            if field.is_relation and field.related_model:
                related_models.add(field.related_model.__name__.lower())
                print(f"[DEBUG] Found related model: {field.related_model.__name__.lower()} for {model.__name__.lower()}")
    return related_models


def get_group_permissions(user):
    """
    Fetch all permissions from user groups and cache them.
    Returns a dictionary mapping models to their allowed actions.
    """
    cache_key = f"user_{user.id}_group_permissions"
    group_permissions = cache.get(cache_key)

    if group_permissions is None:
        group_permissions = {}
        for group in user.groups.all():
            for perm in group.permissions.all():
                try:
                    action, model_name = perm.codename.split("_", 1)  
                    if model_name not in group_permissions:
                        group_permissions[model_name] = set()
                    group_permissions[model_name].add(action)
                except ValueError:
                    logger.warning(f"Invalid permission codename: {perm.codename}")
                    continue 

        cache.set(cache_key, group_permissions, timeout=60)  
    return group_permissions

class DynamicModelPermission(BasePermission):
    """
    Dynamic permission class ensuring:
    - Users can only perform actions if they have explicit permissions.
    - Related models (ManyToMany, ForeignKey) require CRU permissions when adding or updating.
    - Superusers have full access, except deleting their own account.
    - Certain models are restricted for deletion or public listing.
    """

    def has_permission(self, request, view):
        model_name = getattr(view.queryset.model, "__name__", "").lower()

        if not model_name:
            print(f"[DEBUG] Unable to determine model name for view: {view}")
            return False

        # ✅ Allow public access to 'list' and 'retrieve' actions
        if view.action in ["list", "retrieve"]:
            print(f"[DEBUG] Allowing public access to {view.action} for model: {model_name}")
            return True  # ✅ Always allow public viewing

        group_permissions = get_group_permissions(request.user)

        # Restrict other actions based on permissions
        if model_name not in group_permissions:
            print(f"[DEBUG] User {request.user.id} has NO permissions for model: {model_name}")
            return False

        required_permission = ACTION_PERMISSION_MAPPING.get(view.action, None)
        if required_permission and required_permission not in group_permissions[model_name]:
            print(f"[DEBUG] User {request.user.id} lacks required permission: {required_permission} for model: {model_name}")
            return False

        return True



    def get_group_permissions(user):
        cache_key = f"user_{user.id}_group_permissions"
        group_permissions = cache.get(cache_key)

        if group_permissions is None:
            group_permissions = {}
            for group in user.groups.all():
                print(f"[DEBUG] Checking permissions for group: {group.name}")
                for perm in group.permissions.all():
                    try:
                        action, model_name = perm.codename.split("_", 1)
                        if model_name not in group_permissions:
                            group_permissions[model_name] = set()
                        group_permissions[model_name].add(action)
                        print(f"[DEBUG] User {user.id} has permission: {action}_{model_name}")
                    except ValueError:
                        print(f"[DEBUG] Invalid permission codename: {perm.codename}")
                        continue 

            # ✅ Ensure CRU permissions on related models
            for model_name in list(group_permissions.keys()):
                related_models = get_related_models(ALL_MODELS.get(model_name))
                for related_model in related_models:
                    if related_model not in group_permissions:
                        group_permissions[related_model] = {"view", "add", "change"}
                        print(f"[DEBUG] Auto-adding CRU permissions for related model: {related_model}")

            cache.set(cache_key, group_permissions, timeout=60)  

        return group_permissions

