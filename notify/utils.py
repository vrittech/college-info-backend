from .models import Notification
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from .middleware import get_current_user  # Import user context

def notify_user(action, instance):
    """
    Creates a notification for a user only if they have permissions.
    """
    if not hasattr(instance, '_meta'):
        return  # Prevent recursion errors

    user = get_current_user()  # Automatically fetch request user
    if not user:
        return  # Skip if user is unknown

    model_name = instance._meta.model_name.lower()
    identifier = getattr(instance, 'slug', instance.id)  # Use slug if available, otherwise ID

    # Define action messages
    action_messages = {
        'created': f"{user.get_full_name()} added a new {model_name} item.",
        'updated': f"{user.get_full_name()} updated a {model_name} item.",
        'deleted': f"{user.get_full_name()} deleted a {model_name} item.",
    }

    title = f"{model_name.capitalize()} {action.capitalize()}"
    message = action_messages[action]

    # Fetch model permissions dynamically
    content_type = ContentType.objects.get_for_model(instance.__class__)
    permission_codename = f'view_{model_name}'
    user_has_permission = user.has_perm(f"{instance._meta.app_label}.{permission_codename}")

    if not user_has_permission:
        return  # Skip if user lacks permission

    # Create the notification
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        module_name=instance._meta.app_label,
        updated_id=str(identifier),
        timestamp=now(),
    )
