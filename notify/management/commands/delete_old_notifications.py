from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notify.models import Notification  # Replace with your actual Notification model

class Command(BaseCommand):
    help = "Deletes notifications older than 7 days."

    def handle(self, *args, **kwargs):
        # Calculate the date 7 days ago
        cutoff_date = timezone.now() - timedelta(days=7)

        # Delete notifications older than 7 days
        deleted_count, _ = Notification.objects.filter(timestamp__lt=cutoff_date).delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} old notifications."))