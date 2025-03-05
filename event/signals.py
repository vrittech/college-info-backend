from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event

@receiver(post_save, sender=Event)
def set_position_same_as_id(sender, instance, created, **kwargs):
    if created and instance.position != instance.id:
        instance.position = instance.id
        instance.save()
