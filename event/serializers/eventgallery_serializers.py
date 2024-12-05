from rest_framework import serializers
from ..models import EventGallery

class EventGalleryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = '__all__'

class EventGalleryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = '__all__'

class EventGalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = '__all__'