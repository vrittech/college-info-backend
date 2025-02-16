from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib.auth.models import User
from django.apps import apps

# 📌 Generic function to send notifications
def send_notification(instance, action, recipient=None, additional_info=None):
    """ Sends notifications for all CRUD actions (only to the relevant user) """
    # For example, assume that each model has a `user` field indicating the owner or relevant user
    if hasattr(instance, 'user'):  # Check if the model has a `user` field (modify this as needed)
        recipient = instance.user  # The user associated with this instance (model)
    
    # If there's no `user` attribute, you can customize how you determine the recipient
    else:
        # Example: if there's a creator or owner field, you can notify that user instead
        pass
    
    if not recipient:
        return  # If there's no recipient defined, don't send any notifications
    
    # Construct the message based on the action
    if action == 'created':
        verb = "created"
        description = f"A new {instance.__class__.__name__} was created."
    elif action == 'updated':
        verb = "updated"
        description = f"The {instance.__class__.__name__} was updated."
    elif action == 'deleted':
        verb = "deleted"
        description = f"The {instance.__class__.__name__} was deleted."

    # Add additional info to description if available
    if additional_info:
        description += f" Additional Info: {additional_info}"

    # Check if the actor (user) is a superadmin
    if instance.user and instance.user.is_superuser:
        # If the actor is a superadmin, send notifications to all users
        all_users = User.objects.all()
        for user in all_users:
            notify.send(
                instance.user,  # Actor (superadmin who triggered the action)
                recipient=user,  # All users will be notified
                verb=verb,
                description=description
            )
    else:
        # Send notification to the specific recipient
        notify.send(
            instance.user,  # Actor (the user who triggered the action)
            recipient=recipient,
            verb=verb,
            description=description
        )

# 📌 Dynamically connect signals for all models
def connect_signals():
    for model in apps.get_models():  # Get all models in the project
        if hasattr(model, 'user'):  # Filter models with 'user' field (you can modify this)
            # Handle post_save (creation and updates)
            post_save.connect(handle_save, sender=model)

            # Handle post_delete (deletion)
            post_delete.connect(handle_delete, sender=model)

# 📌 Handle post_save signals (for creation or updates)
@receiver(post_save)
def handle_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    send_notification(instance, action, recipient=None)

# 📌 Handle post_delete signals (for deletions)
@receiver(post_delete)
def handle_delete(sender, instance, **kwargs):
    send_notification(instance, action='deleted', recipient=None)

# 📌 Automatically call connect_signals function to register signals when Django starts
connect_signals()
