from rest_framework import serializers
from notifications.models import Notification  # The Notification model from django-notifications-hq

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "recipient", "actor", "verb", "description", "timestamp", "unread"]
