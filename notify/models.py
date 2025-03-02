from django.db import models
from accounts.models import CustomUser as User
from django.utils.timezone import now

from django.db import models
from accounts.models import CustomUser as User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    title = models.CharField(max_length=255)
    casual_message = models.TextField(blank=True, null=True)
    detailed_message = models.TextField(blank=True, null=True)
    module_name = models.CharField(max_length=255, blank=True, null=True)
    updated_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_notifications', blank=True)

    def __str__(self):
        return self.title