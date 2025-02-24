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
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )  # Accept multiple image uploads

    class Meta:
        model = CollegeGallery
        fields = ['images', 'description']  # Keep `images` as input, but use `image` in DB

    def to_representation(self, instance):
        """
        Ensures `images` is used instead of `image` in responses.
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

        while f'image[{index}]' in request.FILES:
            images.append(request.FILES[f'image[{index}]'])
            index += 1

        college = self.context.get('college')  # Get college from context if needed
        gallery_instances = []

        for image in images:
            gallery_instance = CollegeGallery.objects.create(image=image, college=college)
            gallery_instances.append(gallery_instance)

        return gallery_instances[0] if gallery_instances else None  # Return a single instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = []
        index = 0

        while f'image[{index}]' in request.FILES:
            images.append(request.FILES[f'image[{index}]'])
            index += 1

        for image in images:
            CollegeGallery.objects.create(image=image, college=instance.college)

        return super().update(instance, validated_data)