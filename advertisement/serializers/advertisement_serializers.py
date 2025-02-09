from rest_framework import serializers
from ..models import Advertisement,PlacementPosition

class PlacementPositionSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlacementPosition
        fields = '__all__'

class AdvertisementListSerializers(serializers.ModelSerializer):
    placement = PlacementPositionSerializers(read_only=True)
    class Meta:
        model = Advertisement
        fields = '__all__'

class AdvertisementRetrieveSerializers(serializers.ModelSerializer):
    placement = PlacementPositionSerializers(read_only=True)
    class Meta:
        model = Advertisement
        fields = '__all__'

class AdvertisementWriteSerializers(serializers.ModelSerializer):
    # placement = PlacementPositionSerializers()
    class Meta:
        model = Advertisement
        fields = '__all__'