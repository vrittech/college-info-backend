# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from notifications.signals import notify
# from django.apps import apps
# from django.contrib.auth import get_user_model
# import logging
# from django.contrib.admin.models import LogEntry
# from notifications.models import Notification  
# from django.utils.timezone import now
# from django.db import models

# # Logger setup for debugging
# logger = logging.getLogger(__name__)

# User = get_user_model()  # Get custom user model dynamically

# # Default system actor (fallback if no valid actor is found)
# SYSTEM_ACTOR, _ = User.objects.get_or_create(username="System", defaults={"email": "system@domain.com"})


# # 📌 Function to send notifications
# def send_notification(instance, action, recipient=None, additional_info=None, request=None):
#     """ Sends notifications for all CRUD actions (always saves notifications) """
    
#     # Skip notifications for LogEntry (admin activity logs)
#     if isinstance(instance, LogEntry):
#         return

#     # Ensure instance is a valid Django model
#     if not isinstance(instance, models.Model):
#         print(f"❌ Invalid instance received: {instance}. Skipping notification.")
#         return

#     model_name = instance._meta.model_name.capitalize()

#     # Construct notification message
#     action_messages = {
#         "created": f"A new {model_name} was created.",
#         "updated": f"The {model_name} was updated.",
#         "deleted": f"The {model_name} was deleted."
#     }
#     verb = action
#     description = action_messages.get(action, "Unknown action.")

#     if additional_info:
#         description += f" Additional Info: {additional_info}"

#     # Identify the actor (who performed the action)
#     actor = getattr(instance, 'user', None)

#     # Use request user if available
#     if request and hasattr(request, "user") and request.user.is_authenticated:
#         actor = request.user

#     # If actor is still None, use SYSTEM_ACTOR as fallback
#     if not isinstance(actor, models.Model):
#         actor = SYSTEM_ACTOR
#         print(f"⚠️ No valid actor found, using SYSTEM_ACTOR: {actor}")

#     print(f"✅ Sending notification: actor={actor}, recipient={recipient}, verb={verb}, description={description}")

#     # If no specific recipient is provided, send to all users
#     if recipient is None:
#         all_users = User.objects.exclude(id=actor.id)  # Exclude self-notifications
#         for user in all_users:
#             notify.send(actor, recipient=user, verb=verb, description=description)
#             print(f"✅ Notification sent to {user} for action {action}")
#     else:
#         notify.send(actor, recipient=recipient, verb=verb, description=description)
#         print(f"✅ Notification sent to {recipient} for action {action}")

#     print(f"✅ Notification successfully saved: Actor={actor}, Recipient={recipient}, Action={verb}")


# # 📌 Handle post_save signals (for creation or updates)
# @receiver(post_save)
# def handle_save(sender, instance, created, **kwargs):
#     """ Handle object creation or update notifications """
#     action = 'created' if created else 'updated'

#     print(f"🔄 Saving {instance.__class__.__name__} instance, Action: {action}")

#     send_notification(instance, action, recipient=None, request=kwargs.get('request'))


# # 📌 Handle post_delete signals (for deletions)
# @receiver(post_delete)
# def handle_delete(sender, instance, **kwargs):
#     """ Handle object deletion notifications """
#     print(f"🗑️ Deleting {instance.__class__.__name__} instance")

#     send_notification(instance, action='deleted', recipient=None, request=kwargs.get('request'))


# # 📌 Dynamically connect signals for all models
# def connect_signals():
#     for model in apps.get_models():
#         post_save.connect(handle_save, sender=model, weak=False)
#         post_delete.connect(handle_delete, sender=model, weak=False)
#         print(f"✅ Signals connected for model: {model.__name__}")


# # 📌 Automatically register signals when Django starts
# connect_signals()
