from rest_framework import serializers
from .models import Notification
from accounts.models import CustomUser as User
from django.utils.timezone import localtime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class NotificationSerializer(serializers.ModelSerializer):
    # Custom fields
    user_details = serializers.SerializerMethodField(read_only=True)
    formatted_timestamp = serializers.SerializerMethodField(read_only=True)
    is_read = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'user_details',  # Custom field
            'title',
            'casual_message',
            'detailed_message',
            'module_name',
            'updated_id',
            'timestamp',
            'formatted_timestamp',  # Custom field
            'read_by',  # Users who have read the notification
            'is_read',  # Custom field to check if the current user has read the notification
        ]
        read_only_fields = ['id', 'timestamp', 'user_details', 'formatted_timestamp', 'is_read']

    def get_user_details(self, obj):
        """
        Return user details using the UserSerializer.
        """
        user = obj.user
        return UserSerializer(user).data

    def get_formatted_timestamp(self, obj):
        """
        Return a formatted timestamp.
        """
        local_timestamp = localtime(obj.timestamp)  # Converts to local timezone (from settings.py)
        return local_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def get_is_read(self, obj):
        """
        Check if the current user has read the notification.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.read_by.all()
        return False