from rest_framework import serializers
from ..models import CollegeGallery, College

### ✅ College Serializer for nested relation ###
class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        ref_name = 'CollegeGallerySerializers'
        fields = ['slug', 'id', 'name']


### ✅ Read Serializer (for Listing Multiple Galleries) ###
class CollegeGalleryListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    images = serializers.SerializerMethodField()  # Ensures `images` is the response key

    class Meta:
        model = CollegeGallery
        fields = ['id', 'college', 'images', 'description', 'created_date', 'updated_date']

    def get_images(self, obj):
        """Returns a list of image URLs for consistency."""
        return [obj.image.url] if obj.image else []


### ✅ Read Serializer (for Retrieving a Single Gallery) ###
class CollegeGalleryRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    images = serializers.SerializerMethodField()  # Ensures `images` is the response key

    class Meta:
        model = CollegeGallery
        fields = ['id', 'college', 'images', 'description', 'created_date', 'updated_date']

    def get_images(self, obj):
        """Returns a list of image URLs for consistency."""
        return [obj.image.url] if obj.image else []


### ✅ Write Serializer (Handles Multi-Image Uploads) ###
class CollegeGalleryWriteSerializers(serializers.ModelSerializer):

    class Meta:
        model = CollegeGallery
        fields = ['images', 'description']  # `images` key remains consistent in responses

    def to_representation(self, instance):
        """
        Ensures the response uses `images` instead of `image` for consistency.
        """
        return {
            "id": instance.id,
            "images": [instance.image.url] if instance.image else [],
            "description": instance.description
        }

    def create(self, validated_data):
        request = self.context.get('request')
        images = []
        index = 0

        # ✅ Handling `image[0]`, `image[1]`, etc.
        while f'images[{index}]' in request.FILES:
            images.append(request.FILES[f'images[{index}]'])
            index += 1

        college = self.context.get('college')  # Get college from context if needed
        gallery_instances = []

        for image in images:
            gallery_instance = CollegeGallery.objects.create(image=image, college=college)
            gallery_instances.append(gallery_instance)

        return gallery_instances[0] if gallery_instances else None  # Return single instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = []
        index = 0

        # ✅ Handling `image[0]`, `image[1]`, etc.
        while f'images[{index}]' in request.FILES:
            images.append(request.FILES[f'images[{index}]'])
            index += 1

        for image in images:
            CollegeGallery.objects.create(image=image, college=instance.college)

        return super().update(instance, validated_data)
