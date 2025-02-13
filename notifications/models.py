from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for better performance
    module_name = models.CharField(max_length=100, db_index=True)
    updated_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)  # Indexed for search
    users = models.ManyToManyField(CustomUser, related_name="notifications", through="NotificationUser")  # Track read status

    def __str__(self):
        return f"{self.title} - {self.module_name}"

    class Meta:
        permissions = [
            ('can_manage_notifications', 'Can manage notifications'),
        ]

class NotificationUser(models.Model):
    """
    Intermediate model to track if a user has read a notification.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'notification')  # Ensures no duplicate user-notification entries

    def mark_as_read(self):
        """Marks this notification as read for the user and sets a timestamp."""
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.notification.title} ({'Read' if self.is_read else 'Unread'})"
