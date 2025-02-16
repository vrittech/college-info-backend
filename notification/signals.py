from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.signals import notify
from django.apps import apps
from django.contrib.auth import get_user_model
import logging
from mainproj.permissions import get_group_permissions
from accounts.models import CustomUser as User
from django.contrib.admin.models import LogEntry
from notifications.models import Notification  
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

# Logger setup for debugging
logger = logging.getLogger(__name__)

# Action-to-Permission Mapping
ACTION_PERMISSION_MAPPING = {
    "list": "view",  
    "retrieve": "view",
    "create": "add",
    "update": "change",
    "partial_update": "change",
    "destroy": "delete",
}

# Function to send notifications based on permissions and action
# Function to send notifications based on permissions and action
def send_notification(instance, action, recipient=None, additional_info=None, request=None):
    """ Sends notifications for all CRUD actions (only to the relevant user) """
    
    # Skip notifications for LogEntry (admin activity logs)
    if isinstance(instance, LogEntry):
        return

    # Ensure that the instance is not None
    if instance is None:
        print(f"Received None instance. Skipping notification.")
        return

    model_name = instance._meta.model_name  # This will return the lowercased name of the model

    # Construct the message based on the action
    if action == 'created':
        verb = "created"
        description = f"A new {model_name.capitalize()} was created."
    elif action == 'updated':
        verb = "updated"
        description = f"The {model_name.capitalize()} was updated."
    elif action == 'deleted':
        verb = "deleted"
        description = f"The {model_name.capitalize()} was deleted."

    # Add additional info to description if available
    if additional_info:
        description += f" Additional Info: {additional_info}"

    # Ensure that the instance has a 'user' attribute, otherwise skip
    actor = getattr(instance, 'user', None)
    
    if actor:
        print(f"Actor found for instance {instance}: {actor}")
    else:
        print(f"No actor found for instance {instance}. Using authenticated user for notification.")

    # If request is provided, use the authenticated user as the actor
    if request and request.user.is_authenticated:
        actor = request.user
        print(f"Authenticated user used as actor: {actor}")
    
    # Ensure actor is not None before proceeding with notification
    if actor is None:
        print(f"Actor is None, skipping notification.")
        return

    # Logging the action details for debugging
    print(f"Sending notification: actor={actor}, recipient={recipient}, verb={verb}, description={description}")

    # If no specific recipient is provided, send to all users
    if recipient is None:
        all_users = User.objects.all()
        for user in all_users:
            # Save the notification data
            notify.send(actor, recipient=user, verb=verb, description=description)
            print(f"Notification sent to {user} for action {action}")
    else:
        # Save the notification data
        notify.send(actor, recipient=recipient, verb=verb, description=description)
        print(f"Notification sent to {recipient} for action {action}")

    # Print model data after saving
    print(f"Notification saved in model: {actor}, {recipient}, {verb}, {description}")




# 📌 Handle post_save signals (for creation or updates)
@receiver(post_save)
def handle_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    
    # Log the model name and action for debugging purposes
    print(f"Saving {instance.__class__.__name__} instance, Action: {action}")

    send_notification(instance, action, recipient=None, request=kwargs.get('request'))

# 📌 Handle post_delete signals (for deletions)
@receiver(post_delete)
def handle_delete(sender, instance, **kwargs):
    # Log the model name and deletion for debugging purposes
    print(f"Deleting {instance.__class__.__name__} instance")
    
    send_notification(instance, action='deleted', recipient=None, request=kwargs.get('request'))

# 📌 Dynamically connect signals for all models
def connect_signals():
    for model in apps.get_models():  # Fetch all models dynamically
        if hasattr(model, 'user'):  # Filter models that have a `user` field
            post_save.connect(handle_save, sender=model)
            post_delete.connect(handle_delete, sender=model)
            print(f"Connected signals for model: {model.__name__}")

# 📌 Automatically call connect_signals function to register signals when Django starts
connect_signals()

