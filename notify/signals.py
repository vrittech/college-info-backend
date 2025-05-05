from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from accounts.models import CustomUser as User
from .models import Notification
import json
import requests
from django_currentuser.middleware import get_current_authenticated_user


# Constants
ACTION_CREATED = "created"
ACTION_UPDATED = "updated"
ACTION_DELETED = "deleted"

def get_current_user():
    """
    Retrieve the current request user from middleware (for authenticated users).
    Returns None if the request is from an unauthorized user.
    """
    return get_current_authenticated_user()

def should_notify(instance, action):
    """
    Check if a notification should be sent based on the instance's model and action.
    """
    print(f"Checking if notification should be sent for {instance._meta.model_name} with action: {action}")

    model_name = f"{instance._meta.app_label}.{instance._meta.model_name}".lower()
    notification_models_lower = {k.lower(): v for k, v in settings.NOTIFICATION_MODELS.items()}
    print(f"Model name: {model_name}")
    print(f"NOTIFICATION_MODELS: {notification_models_lower}")

    if model_name in notification_models_lower and action in notification_models_lower[model_name]:
        print(f"Notification should be sent for {model_name} with action: {action}")
        return True

    print(f"Notification should NOT be sent for {model_name} with action: {action}")
    return False

def get_notification_receivers(instance, user):
    """
    Determine notification recipients.
    - If the user is authenticated, notify the user and superadmins.
    - If the user is not authenticated, notify superadmins only.
    """
    print(f"Determining notification receivers for {instance._meta.model_name}")

    receivers = []
    
    if user and user.is_authenticated:
        print(f" User is authenticated: {user.email}")
        receivers.append(user)  # Notify the user themselves
    else:
        print(f"User is not authenticated or no user found.")

    # Always notify superadmins
    superadmins = User.objects.filter(is_superuser=True)
    print(f"Superadmins to notify: {superadmins.count()}")
    receivers.extend(superadmins)

    print(f"Final receivers: {[r.email for r in receivers]}")
    return list(set(receivers))  # Remove duplicates

def create_notification(instance, action, user):
    """
    Generic function to create a notification with both casual and detailed messages.
    """
    print(f"Creating notification for {instance._meta.model_name} with action: {action}")

    model_name = instance._meta.model_name.lower()
    identifier = str(getattr(instance, 'slug', getattr(instance, 'id', 'unknown')))
    title = f"{model_name.capitalize()} {action.capitalize()}"

    # Casual message (short and user-friendly)
    casual_message = f"{user.first_name} {action} a {model_name}." if user and user.is_authenticated else f"A {model_name} was {action} by an unauthorized user."

    # Detailed message (includes object data)
    object_data = {
        "id": instance.id,
        "name": getattr(instance, 'name', 'Unnamed'),
        "created_at": now().isoformat(),
    }
    detailed_message = f"{casual_message} Details: {json.dumps(object_data, indent=2)}"

    permission_codename = f"{instance._meta.app_label}.view_{model_name}"
    print(f"🔍 Permission codename: {permission_codename}")

    receivers = get_notification_receivers(instance, user)
    try:
        notifications = [
            Notification(
                user=receiver,
                title=title,
                casual_message=casual_message,  # Casual message
                detailed_message=detailed_message,  # Detailed message
                module_name=instance._meta.app_label,
                updated_id=identifier,
                timestamp=now(),
            )
            for receiver in receivers if receiver.has_perm(permission_codename) or model_name in settings.PUBLIC_NOTIFICATION_MODELS
        ]
        print(f"Notifications to create: {len(notifications)}")
        Notification.objects.bulk_create(notifications)
        print(f"Notifications successfully created for {len(notifications)} receivers")
    except Exception as e:
        print(f"Error creating notification: {e}")

@receiver(post_save)
def handle_post_save(sender, instance, created, **kwargs):
    """
    Handle post_save signal to create notifications for successful creations or updates.
    """
    print(f"post_save signal triggered for {sender.__name__}")

    action = ACTION_CREATED if created else ACTION_UPDATED
    if should_notify(instance, action):
        print(f"Should notify for {sender.__name__} with action: {action}")
        user = get_current_user()
        create_notification(instance, action, user)
    else:
        print(f"Should NOT notify for {sender.__name__} with action: {action}")

@receiver(post_delete)
def handle_post_delete(sender, instance, **kwargs):
    """
    Handle post_delete signal to create notifications for successful deletions.
    """
    print(f"post_delete signal triggered for {sender.__name__}")

    if should_notify(instance, ACTION_DELETED):
        print(f"Should notify for {sender.__name__} with action: {ACTION_DELETED}")
        user = get_current_user()
        create_notification(instance, ACTION_DELETED, user)
    else:
        print(f"Should NOT notify for {sender.__name__} with action: {ACTION_DELETED}")