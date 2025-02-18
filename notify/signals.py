from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.apps import apps
from accounts.models import CustomUser
from .models import Notification

def get_users_with_permission(model_name, app_label):
    """
    Fetch users who have the 'view_{model_name}' permission.
    Includes both individual permissions and those granted via groups.
    """
    content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
    permission_codename = f'view_{model_name.lower()}'
    
    try:
        permission = Permission.objects.get(content_type=content_type, codename=permission_codename)
    except Permission.DoesNotExist:
        return CustomUser.objects.none()  # Return empty queryset if permission doesn't exist

    # Get users with direct permission
    users = CustomUser.objects.filter(user_permissions=permission)

    # Get users who belong to groups with the required permission
    users_in_groups = CustomUser.objects.filter(groups__permissions=permission)

    # Merge both user lists and remove duplicates
    return users.union(users_in_groups).distinct()


def create_notification(action, instance, user):
    """
    Create a notification only for users who have the correct permissions.
    Uses GenericForeignKey for better object reference.
    """
    model_name = instance._meta.model_name
    app_label = instance._meta.app_label

    users_with_permission = get_users_with_permission(model_name, app_label)

    if not users_with_permission.exists():
        return  # No need to create notifications if no user has permission

    # Identify object uniquely
    object_identifier = getattr(instance, 'slug', instance.pk)

    # Define a more specific notification message
    action_messages = {
        'created': f"{user.get_full_name()} added a new {model_name} in {app_label}.",
        'updated': f"{user.get_full_name()} updated {model_name} in {app_label}.",
        'deleted': f"{user.get_full_name()} deleted {model_name} from {app_label}."
    }

    # Create notifications in bulk
    notifications = [
        Notification(
            title=f"{model_name.capitalize()} {action.capitalize()}",
            message=action_messages[action],
            module_name=app_label,
            updated_id=str(object_identifier),
            timestamp=now()
        )
        for user in users_with_permission
    ]

    Notification.objects.bulk_create(notifications)


@receiver(post_save)
def handle_create_update_notifications(sender, instance, created, **kwargs):
    """
    Handles create and update events dynamically.
    Uses `updated_by` field to track which user performed the action.
    """
    if not hasattr(instance, '_meta'):
        return  # Skip non-model instances

    model_name = instance._meta.model_name
    user = getattr(instance, 'updated_by', None)  # Ensure models have `updated_by`

    if not user or not isinstance(user, CustomUser):
        return  # Skip if no user is associated with the action

    action = 'created' if created else 'updated'
    create_notification(action, instance, user)


@receiver(post_delete)
def handle_delete_notifications(sender, instance, **kwargs):
    """
    Handles delete events dynamically.
    Uses `deleted_by` field to track the user who performed the delete action.
    """
    if not hasattr(instance, '_meta'):
        return  # Skip non-model instances

    model_name = instance._meta.model_name
    user = getattr(instance, 'deleted_by', None)  # Ensure models have `deleted_by`

    if not user or not isinstance(user, CustomUser):
        return  # Skip if no user is associated with the action

    create_notification('deleted', instance, user)
