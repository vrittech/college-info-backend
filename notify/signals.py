from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from django.apps import apps
from accounts.models import CustomUser as User
from .models import Notification


def get_current_user():
    """
    Retrieve the current request user from middleware.
    """
    from .middleware import get_current_user
    return get_current_user()

def should_notify(instance, action):
    """
    Checks if the model should trigger notifications based on settings.
    """
    model_name = f"{instance._meta.app_label}.{instance._meta.model_name}"
    return model_name in settings.NOTIFICATION_MODELS and action in settings.NOTIFICATION_MODELS[model_name]

@receiver(post_save)
def create_update_notification(sender, instance, created, **kwargs):
    """
    Create notifications dynamically when an instance is created or updated.
    """
    if not hasattr(instance, '_meta'):
        return

    action = "created" if created else "updated"
    if not should_notify(instance, action):
        return  # Skip notification if the model/action is not in settings

    user = get_current_user()
    if not user or not user.is_authenticated:
        return  # Skip if user is not authenticated

    model_name = instance._meta.model_name.lower()
    identifier = str(getattr(instance, 'slug', getattr(instance, 'id', 'unknown')))

    message = f"{user.get_full_name()} {action} a {model_name}."
    title = f"{model_name.capitalize()} {action.capitalize()}"

    permission_codename = f"{instance._meta.app_label}.view_{model_name}"
    if not user.has_perm(permission_codename):
        return  # Skip if user lacks permission

    # Create notification
    Notification.objects.create(
        user=user,
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
    """
    if not hasattr(instance, '_meta'):
        return

    if not should_notify(instance, "deleted"):
        return  # Skip notification if the model/action is not in settings

    user = get_current_user()
    if not user or not user.is_authenticated:
        return  # Skip if user is not authenticated

    model_name = instance._meta.model_name.lower()
    identifier = str(getattr(instance, 'slug', getattr(instance, 'id', 'unknown')))

    title = f"{model_name.capitalize()} Deleted"
    message = f"{user.get_full_name()} deleted a {model_name}."

    permission_codename = f"{instance._meta.app_label}.view_{model_name}"
    if not user.has_perm(permission_codename):
        return  # Skip if user lacks permission

    # Create notification
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        module_name=instance._meta.app_label,
        updated_id=identifier,
        timestamp=now(),
    )
