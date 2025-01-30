from rest_framework import serializers
from django.db import transaction

from ..models import Information, Level, SubLevel, Course, Affiliation, District, College, Faculty, InformationTagging, InformationCategory, InformationGallery, InformationFiles

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        ref_name = 'levels'
        fields = '__all__'

class SubLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        ref_name = 'sublevels'
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        ref_name = 'affiliations'
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        ref_name = 'districts'
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        ref_name = 'colleges'
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        ref_name = 'faculties'
        fields = '__all__'

class InformationTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationTagging
        ref_name = 'information_taggings'
        fields = '__all__'

class InformationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        ref_name = 'information_categories'
        fields = '__all__'

# 🔹 Serializers for File & Image Uploads
class InformationGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationGallery
        ref_name = 'information_galleries'
        fields = '__all__'

class InformationFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationFiles
        ref_name = 'information_files'
        fields = '__all__'

class InformationTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationTagging
        ref_name = 'information_taggings'
        fields = '__all__'


class InformationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        ref_name = 'information_categories'
        fields = '__all__'


class InformationGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationGallery
        ref_name = 'information_galleries'
        fields = '__all__'


class InformationListSerializers(serializers.ModelSerializer):
    level = LevelSerializer(many=True, read_only=True)
    sublevel = SubLevelSerializer(many=True, read_only=True)
    course = CourseSerializer(many=True, read_only=True)
    affiliation = AffiliationSerializer(many=True, read_only=True)
    district = DistrictSerializer(many=True, read_only=True)
    college = CollegeSerializer(many=True, read_only=True)
    faculty = FacultySerializer(many=True, read_only=True)
    information_tagging = InformationTaggingSerializer(many=True, read_only=True)
    information_category = InformationCategorySerializer(many=True, read_only=True)
    
    information_gallery = InformationGallerySerializer(many=True, read_only=True, source='informationgallery_set')
    information_files = InformationFilesSerializer(many=True, read_only=True, source='informationfiles_set')

    class Meta:
        model = Information
        fields = '__all__'


class InformationRetrieveSerializers(serializers.ModelSerializer):
    level = LevelSerializer(many=True, read_only=True)
    sublevel = SubLevelSerializer(many=True, read_only=True)
    course = CourseSerializer(many=True, read_only=True)
    affiliation = AffiliationSerializer(many=True, read_only=True)
    district = DistrictSerializer(many=True, read_only=True)
    college = CollegeSerializer(many=True, read_only=True)
    faculty = FacultySerializer(many=True, read_only=True)
    information_tagging = InformationTaggingSerializer(many=True, read_only=True)
    information_category = InformationCategorySerializer(many=True, read_only=True)
    
    information_gallery = InformationGallerySerializer(many=True, read_only=True, source='informationgallery_set')
    information_files = InformationFilesSerializer(many=True, read_only=True, source='informationfiles_set')
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
            elif key.startswith('files['):  # Files in array format
                files_data.append(file)

        # Create the Information instance
        information = super().create(validated_data)

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
            elif key.startswith('files['):  # Files in array format
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
