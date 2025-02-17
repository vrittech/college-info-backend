from rest_framework import serializers
from ..models import CollegeGallery,College

class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['slug','id','name']

class CollegeGalleryListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    class Meta:
        model = CollegeGallery
        fields = '__all__'

class CollegeGalleryRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    class Meta:
        model = CollegeGallery
        fields = '__all__'

class CollegeGalleryWriteSerializers(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = CollegeGallery
        fields = ['images', 'description']  # Excluding 'image' field since we're handling multiple images

    def create(self, validated_data):
        request = self.context.get('request')
        images = []
        index = 0

        while f'image[{index}]' in request.FILES:
            images.append(request.FILES[f'image[{index}]'])
            index += 1

        gallery_instances = []
        for image in images:
            gallery_instance = CollegeGallery.objects.create(image=image)
            gallery_instances.append(gallery_instance)

        return gallery_instances

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = []
        index = 0

        while f'image[{index}]' in request.FILES:
            images.append(request.FILES[f'image[{index}]'])
            index += 1

        for image in images:
            CollegeGallery.objects.create(image=image)

        return super().update(instance, validated_data)
