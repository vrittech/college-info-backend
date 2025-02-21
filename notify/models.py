from django.db import models
from accounts.models import CustomUser as User
from django.utils.timezone import now

class Notification(models.Model):
    """
    Stores notifications dynamically for configured models only.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    module_name = models.CharField(max_length=100)  # Example: 'students', 'courses'
    updated_id = models.CharField(max_length=100)  # Unique identifier (slug or ID)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification: {self.title} - {self.message}"
