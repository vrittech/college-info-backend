from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventGallery
# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Event
from datetime import datetime


@receiver(post_save, sender=EventGallery)
def set_position_same_as_id(sender, instance, created, **kwargs):
    if created and instance.position != instance.id:
        instance.position = instance.id
        instance.save()

@receiver(pre_save, sender=Event)
def check_event_expiration(sender, instance, **kwargs):
    """
    Update the is_expired field based on the end_date.
    This will be triggered whenever an Event is saved.
    """
    if instance.end_date and instance.end_date < datetime.now():
        instance.is_expired = True
    else:
        instance.is_expired = False
