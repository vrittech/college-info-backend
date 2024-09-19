from rest_framework import serializers
from ..models import Image

class ImageListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ImageRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ImageWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'