from rest_framework import serializers
from ..models import Advertisement

class AdvertisementListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

class AdvertisementRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

class AdvertisementWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'