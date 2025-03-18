from rest_framework import serializers
from ..models import Gallery, Album
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import serializers
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from urllib.parse import urljoin

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'featured_image', 'created_date', 'updated_date']


class GalleryListSerializers(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)

    class Meta:
        model = Gallery
        fields = ['id', 'image', 'album', 'is_cover', 'created_date', 'created_date_time', 'updated_date_time']


class GalleryRetrieveSerializers(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)  # Nested Album objects for the gallery

    class Meta:
        model = Gallery
        fields = ['id', 'image', 'album', 'is_cover', 'created_date', 'created_date_time', 'updated_date_time']


class GalleryWriteSerializers(serializers.ModelSerializer):
    
    """
    Serializer for handling gallery image uploads.
    - Accepts `album` as an ID in the request.
    - Accepts multiple images using `image[0]`, `image[1]`, etc.
    """

    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        write_only=True
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ['id', 'image', 'album', 'is_cover', 'created_date', 'created_date_time', 'updated_date_time']
        
    def get_image(self, obj):
        """ Returns the full image URL """
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        """
        Handles multiple image uploads and ensures the first image is the cover.
        """
        request = self.context.get("request")

        # Retrieve album ID from request data
        album_id = request.data.get("album")  
        if not album_id:
            raise serializers.ValidationError({"album": "This field is required."})

        # Fetch album object
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            raise serializers.ValidationError({"album": "Invalid album ID."})

        # Extract multiple images using keys like `image[0]`, `image[1]`
        uploaded_files = [
            request.FILES[key] for key in request.FILES if key.startswith("image[")
        ]

        if not uploaded_files:
            return []

        # Check if this album already has a cover image
        has_cover = Gallery.objects.filter(album=album, is_cover=True).exists()

        gallery_instances = []
        if uploaded_files:
            for index, image_file in enumerate(uploaded_files):
                if isinstance(image_file, InMemoryUploadedFile):
                    is_first_image = index == 0 and not has_cover  # Ensure first image is cover
                    
                    # Create gallery instance but DO NOT access `.image.url` yet
                    gallery_instance = Gallery(album=album, image=image_file, is_cover=is_first_image)
                    gallery_instance.save()  # Explicitly save the instance first
                    
                    gallery_instances.append(gallery_instance)

                    # Ensure the image field is saved before accessing `.url`
                    if is_first_image and request:
                        gallery_instance.refresh_from_db()  # Ensure fresh data
                        absolute_url = request.build_absolute_uri(gallery_instance.image.url)  # Correct absolute URL
                        
                        # Update album's featured image
                        album.featured_image = absolute_url
                        album.save(update_fields=['featured_image'])

        return gallery_instances

    def update(self, instance, validated_data):
        """
        Handles updating an album by adding new images if provided.
        """
        request = self.context.get("request")

        # Check if new images are being added
        uploaded_files = [
            request.FILES[key] for key in request.FILES if key.startswith("image[")
        ]

        if uploaded_files:
            # Add new images to the album
            gallery_instances = []
            for image_file in uploaded_files:
                if isinstance(image_file, InMemoryUploadedFile):
                    gallery_instance = Gallery.objects.create(
                        album=instance.album,  # Keep album association
                        image=image_file,
                        is_cover=validated_data.get("is_cover", False)
                    )
                    gallery_instances.append(gallery_instance)

            return gallery_instances

        # If no new images, proceed with updating existing fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

