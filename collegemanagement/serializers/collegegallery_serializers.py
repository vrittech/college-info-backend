from rest_framework import serializers
from ..models import CollegeGallery

class CollegeGalleryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeGallery
        fields = '__all__'

class CollegeGalleryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeGallery
        fields = '__all__'

class CollegeGalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeGallery
        fields = '__all__'