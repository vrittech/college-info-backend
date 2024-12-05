from rest_framework import serializers
from ..models import PlacementPosition

class PlacementPositionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlacementPosition
        fields = '__all__'

class PlacementPositionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlacementPosition
        fields = '__all__'

class PlacementPositionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlacementPosition
        fields = '__all__'