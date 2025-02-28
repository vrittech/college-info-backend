from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from django.apps import apps
from accounts.models import CustomUser as User
from .models import Notification
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from django.apps import apps
from accounts.models import CustomUser as User
from .models import Notification
from collegemanagement.models import College  # Import the College model
from django.db.models import ManyToManyField


def dynamic_m2m_notification(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Dynamic handler for all Many-to-Many (M2M) fields.
    """
    print(f"🔄 M2M Changed Signal Triggered → College: {instance.name}, Field: {sender}, Action: {action}")

    if action in ["post_add", "post_remove", "post_clear"]:
        user = get_current_user()
        receivers = get_notification_receivers(instance, user)

        field_name = sender._meta.model_name  # Get the M2M field name dynamically
        title = f"{instance.name} {field_name.capitalize()} Updated"
        message = f"{user.get_full_name()} updated {field_name} for {instance.name}." if user else f"{field_name.capitalize()} were updated for {instance.name}."

        print(f"📨 Attempting to Create Notification → Title: {title}, Message: {message}, Receivers: {receivers}")

        try:
            for receiver in receivers:
                print(f"➡️ Creating notification for {receiver.email}")  # Debugging line
                
                notification = Notification.objects.create(
                    user=receiver,
                    title=title,
                    message=message,
                    module_name=instance._meta.app_label,
                    updated_id=str(instance.id),
                    timestamp=now(),
                )

                print(f"✅ Notification successfully created: {notification}")
        except Exception as e:
            print(f"❌ Error creating notification for M2M update: {e}")



# ✅ Dynamically Connect All M2M Fields in the College Model
for field in College._meta.get_fields():
    if isinstance(field, ManyToManyField) and hasattr(field.remote_field, 'through'):
        try:
            if field.remote_field.through:  # Ensure 'through' is not None
                m2m_changed.connect(dynamic_m2m_notification, sender=field.remote_field.through)
                print(f"✅ Connected m2m_changed signal for {field.name}")
        except AttributeError:
            print(f"❌ Skipping {field.name} - No 'through' attribute")

def get_current_user():
    """
    Retrieve the current request user from middleware (for authenticated users).
    Returns None if the request is from an unauthorized user.
    """
    from .middleware import get_current_user
    return get_current_user()

def should_notify(instance, action):
    model_name = f"{instance._meta.app_label}.{instance._meta.model_name}".lower()

    print(f"🔍 should_notify() → Model Name from Instance: {model_name}, Action: {action}")

    # Ensure NOTIFICATION_MODELS keys are also lowercase
    notification_models_lower = {k.lower(): v for k, v in settings.NOTIFICATION_MODELS.items()}
    print(f"🔎 Checking Against: {list(notification_models_lower.keys())}")

    result = model_name in notification_models_lower and action in notification_models_lower[model_name]

    print(f"✅ Model Found in NOTIFICATION_MODELS? {result}")

    return result





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
    # Print to check the model in NOTIFICATION_MODELS
    print(f"🔍 NOTIFICATION_MODELS: {settings.NOTIFICATION_MODELS}")

    print(f"📢 Signal Triggered: {sender.__name__} - Created: {created}")  # Debugging

    if sender.__name__ not in settings.NOTIFICATION_MODELS:
        print(f"⏩ Skipping: {sender.__name__} not in NOTIFICATION_MODELS")
        return  # Skip if not in notification models

    action = "created" if created else "updated"
    if not should_notify(instance, action):
        print(f"⏩ Skipping: should_notify() returned False for {sender.__name__}")
        return

    user = get_current_user()  # Get request user (None if unauthorized)
    print(f"👤 Current User: {user}")

    receivers = get_notification_receivers(instance, user)
    print(f"📨 Notification Receivers: {receivers}")

    model_name = instance._meta.model_name.lower()
    identifier = str(getattr(instance, 'slug', getattr(instance, 'id', 'unknown')))
    title = f"{model_name.capitalize()} {action.capitalize()}"

    message = f"{user.get_full_name()} {action} a {model_name}." if user and user.is_authenticated else f"A new {model_name} was {action} by an unauthorized user."

    permission_codename = f"{instance._meta.app_label}.view_{model_name}"

    try:
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
                print(f"✅ Notification created for {receiver.email}")
    except Exception as e:
        print(f"❌ Error creating notification: {e}")



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
