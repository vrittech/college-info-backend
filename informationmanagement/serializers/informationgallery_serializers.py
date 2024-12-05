from rest_framework import serializers
from ..models import InformationGallery

class InformationGalleryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationGallery
        fields = '__all__'

class InformationGalleryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationGallery
        fields = '__all__'

class InformationGalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationGallery
        fields = '__all__'