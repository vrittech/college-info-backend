from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from django.apps import apps
from accounts.models import CustomUser as User
from .models import Notification

def get_current_user():
    """
    Retrieve the current request user from middleware (for authenticated users).
    Returns None if the request is from an unauthorized user.
    """
    from .middleware import get_current_user
    return get_current_user()

def should_notify(instance, action):
    """
    Check if the model and action should trigger a notification.
    """
    model_name = f"{instance._meta.app_label}.{instance._meta.model_name}"
    return model_name in settings.NOTIFICATION_MODELS and action in settings.NOTIFICATION_MODELS[model_name]

def get_notification_receivers(instance, user):
    """
    Determine notification recipients:
    - If an `inquiry/contact` is made:
        - If a `college` is associated → Notify **users who have that college field set**.
        - Else → Notify **superadmins**.
    - If an authenticated user performs an action:
        - Notify **themselves**.
        - If they have a `college`, notify **other users from the same college**.
        - Else, notify **superadmins**.
    """
    model_name = f"{instance._meta.app_label}.{instance._meta.model_name}"
    receivers = []

    # 🔹 Case 1: Public User Inquiry (No Authenticated User)
    if model_name in settings.PUBLIC_NOTIFICATION_MODELS:
        college = getattr(instance, 'college', None)
        if college:
            # Notify all users linked to this college (users with college field set to this college)
            receivers = User.objects.filter(college=college)
        else:
            # No college assigned → Notify superadmins
            receivers = User.objects.filter(is_superuser=True)

    # 🔹 Case 2: Authenticated User Action
    elif user and user.is_authenticated:
        receivers = [user]  # Notify the user themselves

        if user.college:
            # Notify all users from the same college
            college_users = User.objects.filter(college=user.college).exclude(id=user.id)
            receivers.extend(college_users)
        else:
            # No college assigned → Notify superadmins
            superadmins = User.objects.filter(is_superuser=True)
            receivers.extend(superadmins)

    return list(set(receivers))  # Remove duplicates

@receiver(post_save)
def create_update_notification(sender, instance, created, **kwargs):
    """
    Create notifications dynamically when an instance is created or updated.
    Handles both authenticated and unauthorized (public) users.
    """
    if sender.__name__ not in settings.NOTIFICATION_MODELS:
        return  # Skip if not in notification models

    action = "created" if created else "updated"
    if not should_notify(instance, action):
        return

    user = get_current_user()  # Get request user (None if unauthorized)

    receivers = get_notification_receivers(instance, user)

    model_name = instance._meta.model_name.lower()
    identifier = str(getattr(instance, 'slug', getattr(instance, 'id', 'unknown')))
    title = f"{model_name.capitalize()} {action.capitalize()}"

    # Handle messages for authenticated and unauthorized users
    if user and user.is_authenticated:
        message = f"{user.get_full_name()} {action} a {model_name}."
    else:
        message = f"A new {model_name} was {action} by an unauthorized user."

    permission_codename = f"{instance._meta.app_label}.view_{model_name}"
    
    for receiver in receivers:
        if receiver.has_perm(permission_codename) or model_name in settings.PUBLIC_NOTIFICATION_MODELS:
            Notification.objects.create(
                user=receiver,
                title=title,
                message=message,
                module_name=instance._meta.app_label,
                updated_id=identifier,
                timestamp=now(),
            )

@receiver(post_delete)
def delete_notification(sender, instance, **kwargs):
    """
    Create notifications dynamically when an instance is deleted.
    Handles both authenticated and unauthorized (public) users.
    """
    if sender.__name__ not in settings.NOTIFICATION_MODELS:
        return  # Skip if not in notification models

    if not should_notify(instance, "deleted"):
        return

    user = get_current_user()  # Get request user (None if unauthorized)

    receivers = get_notification_receivers(instance, user)

    model_name = instance._meta.model_name.lower()
    identifier = str(getattr(instance, 'slug', getattr(instance, 'id', 'unknown')))
    title = f"{model_name.capitalize()} Deleted"

    # Handle messages for authenticated and unauthorized users
    if user and user.is_authenticated:
        message = f"{user.get_full_name()} deleted a {model_name}."
    else:
        message = f"A {model_name} entry was deleted by an unauthorized user."

    permission_codename = f"{instance._meta.app_label}.view_{model_name}"

    for receiver in receivers:
        if receiver.has_perm(permission_codename) or model_name in settings.PUBLIC_NOTIFICATION_MODELS:
            Notification.objects.create(
                user=receiver,
                title=title,
                message=message,
                module_name=instance._meta.app_label,
                updated_id=identifier,
                timestamp=now(),
            )
