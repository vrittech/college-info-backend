from rest_framework import serializers
from ..models import Location

class LocationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'