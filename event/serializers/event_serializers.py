from rest_framework import serializers
from ..models import Event

class EventListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'