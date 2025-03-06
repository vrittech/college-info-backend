from rest_framework import serializers
from ..models import Advertisement,PlacementPosition
from urllib.parse import urljoin
from django.conf import settings

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
    image = serializers.SerializerMethodField()  # Absolute URL for image
    placement = PlacementPositionSerializers()  # Include nested object

    class Meta:
        model = Advertisement
        fields = '__all__'  # Includes all fields + custom fields

    def get_image(self, obj):
        """Returns the absolute URL of the advertisement image"""
        request = self.context.get('request')  # Get request object
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else urljoin(settings.SITE_URL, obj.image.url)
        return None  # If no image
