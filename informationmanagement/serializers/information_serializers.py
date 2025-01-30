from rest_framework import serializers
from django.db import transaction

from ..models import Information, Level, SubLevel, Course, Affiliation, District, College, Faculty, InformationTagging, InformationCategory, InformationGallery, InformationFiles

class InformationTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationTagging
        fields = '__all__'


class InformationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = '__all__'


class InformationGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationGallery
        fields = '__all__'


class InformationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'


class InformationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class InformationWriteSerializers(serializers.ModelSerializer):
    """
    Serializer for handling binary image & file uploads in form-data.
    Many-to-Many fields are managed automatically by Django.
    """

    class Meta:
        model = Information
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        """
        Handles creation of Information instance and processes image & file uploads.
        """
        # Extract images and files from request's FILES
        images_data = []
        files_data = []

        for key, file in self.context['request'].FILES.items():
            if key.startswith('images['):  # Images in array format
                images_data.append(file)
            elif key.startswith('curriculum_file_upload['):  # Files in array format
                files_data.append(file)

        # Create the Information instance
        information = Information.objects.create(**validated_data)

        # Save image uploads
        for image_file in images_data:
            InformationGallery.objects.create(information=information, image=image_file)

        # Save file uploads
        for file_item in files_data:
            InformationFiles.objects.create(information=information, file=file_item)

        return information

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Handles updating an Information instance and manages image & file uploads.
        """
        # Extract images and files from request's FILES
        images_data = []
        files_data = []

        for key, file in self.context['request'].FILES.items():
            if key.startswith('images['):  # Images in array format
                images_data.append(file)
            elif key.startswith('curriculum_file_upload['):  # Files in array format
                files_data.append(file)

        # Update instance fields
        instance = super().update(instance, validated_data)

        # Save new image uploads (append to existing images)
        for image_file in images_data:
            InformationGallery.objects.create(information=instance, image=image_file)

        # Save new file uploads (append to existing files)
        for file_item in files_data:
            InformationFiles.objects.create(information=instance, file=file_item)

        return instance
