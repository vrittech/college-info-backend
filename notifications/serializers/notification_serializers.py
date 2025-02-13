from rest_framework import serializers
from ..models import Notification

class NotificationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'