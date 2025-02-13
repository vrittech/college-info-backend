from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.admin.sites import site
from django.apps import apps
from accounts.models import CustomUser
from .models import Notification, NotificationUser
from django.utils.text import camel_case_to_spaces

def generate_model_map():
    """
    Dynamically generates MODEL_MAP based on models registered in Django Admin,
    excluding built-in apps like auth, contenttypes, sessions, and admin.
    """
    excluded_apps = {'auth', 'contenttypes', 'sessions', 'admin'}
    model_map = {}

    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        class_name = model.__name__

        if app_label not in excluded_apps:
            model_map[model_name] = (app_label, class_name)

    return model_map

MODEL_MAP = generate_model_map()

def notify_users(action, instance, module_name, model_name):
    """
    Helper function to create notifications for users based on the action type.
    """
    identifier = getattr(instance, 'slug', instance.id)  # Use slug if available, else id
    readable_model_name = camel_case_to_spaces(model_name).title()  # Converts to human-readable format

    action_messages = {
        'created': f"A new {readable_model_name} item was added in the {module_name} module.",
        'updated': f"The {readable_model_name} item was updated in the {module_name} module.",
        'deleted': f"The {readable_model_name} item was deleted from the {module_name} module."
    }

    title = f"{readable_model_name} {action.capitalize()}"
    message = action_messages[action]

    permission_codename = f'view_{model_name.lower()}'
    view_permission = Permission.objects.filter(codename=permission_codename)
    users_with_permission = CustomUser.objects.filter(user_permissions__in=view_permission)

    # Create notification
    notification = Notification.objects.create(
        title=title,
        message=message,
        module_name=module_name,
        updated_id=str(identifier)
    )

    # Assign the notification to users & create NotificationUser entries
    for user in users_with_permission:
        NotificationUser.objects.create(user=user, notification=notification)

@receiver(post_save)
def create_or_update_notification(sender, instance, created, **kwargs):
    """
    Signal handler for create and update events.
    """
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    if model_name in MODEL_MAP:
        action = 'created' if created else 'updated'
        notify_users(action, instance, app_label, model_name)

@receiver(post_delete)
def delete_notification(sender, instance, **kwargs):
    """
    Signal handler for delete events.
    """
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    if model_name in MODEL_MAP:
        notify_users('deleted', instance, app_label, model_name)
