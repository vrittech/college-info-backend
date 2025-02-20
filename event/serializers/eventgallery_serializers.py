from rest_framework import serializers
from ..models import EventGallery,Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_name','slug']


class EventGalleryListSerializers(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = EventGallery
        fields = '__all__'

class EventGalleryRetrieveSerializers(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = EventGallery
        fields = '__all__'

class EventGalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = '__all__'