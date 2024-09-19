from rest_framework import serializers
from ..models import EventCategory

class EventCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class EventCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class EventCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'