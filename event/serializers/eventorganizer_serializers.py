from rest_framework import serializers
from ..models import EventOrganizer

class EventOrganizerListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = '__all__'

class EventOrganizerRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = '__all__'

class EventOrganizerWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = '__all__'