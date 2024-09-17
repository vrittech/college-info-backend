from rest_framework import serializers
from ..models import Gallery

class GalleryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'