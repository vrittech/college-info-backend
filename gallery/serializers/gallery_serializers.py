from rest_framework import serializers
from ..models import Gallery, Album
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import serializers


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'featured_image', 'created_date', 'updated_date']


class GalleryListSerializers(serializers.ModelSerializer):
    album = AlbumSerializer(many=True)  # Nested Album objects for the gallery

    class Meta:
        model = Gallery
        fields = ['id', 'image', 'album', 'is_cover', 'created_date', 'created_date_time', 'updated_date_time']


class GalleryRetrieveSerializers(serializers.ModelSerializer):
    album = AlbumSerializer(many=True)  # Nested Album objects for the gallery

    class Meta:
        model = Gallery
        fields = ['id', 'image', 'album', 'is_cover', 'created_date', 'created_date_time', 'updated_date_time']


class GalleryWriteSerializers(serializers.ModelSerializer):
    # The `album` field is written as an integer ID, but the details will be fetched via nested serializer
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), many=True)
    
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'album', 'is_cover', 'created_date', 'created_date_time', 'updated_date_time']
    
    def validate_album(self, value):
        # Validation to ensure album(s) exist
        for album in value:
            if not Album.objects.filter(id=album.id).exists():
                raise serializers.ValidationError(f"Album with id {album.id} does not exist.")
        return value
    
    def create(self, validated_data):
        # Handle the creation of the Gallery instance
        album_data = validated_data.pop('album')
        gallery_instance = Gallery.objects.create(**validated_data)
        
        # Add the albums to the gallery (Many-to-Many relationship)
        gallery_instance.album.set(album_data)
        gallery_instance.save()
        
        return gallery_instance
    
    def update(self, instance, validated_data):
        # Handle the update of an existing Gallery instance
        album_data = validated_data.pop('album', None)
        
        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # If `album` is provided, update the many-to-many relationship
        if album_data is not None:
            instance.album.set(album_data)  # Update the albums associated with the gallery
        
        instance.save()
        return instance
