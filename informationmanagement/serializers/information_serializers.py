from rest_framework import serializers
from django.db import transaction
import ast

from ..models import Information, Level, SubLevel, Course, Affiliation, District, College, Faculty, InformationTagging, InformationCategory, InformationGallery, InformationFiles

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        ref_name = 'levels'
        fields = ['id', 'name']

class SubLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        ref_name = 'sublevels'
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name','slug']

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        ref_name = 'affiliations'
        fields =['id', 'name','slug']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        ref_name = 'districts'
        fields = fields = ['id', 'name']

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        ref_name = 'colleges'
        fields = ['id', 'name','slug']

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        ref_name = 'faculties'
        fields = ['id', 'name']

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
    
    information_gallery = InformationGallerySerializer(many=True, read_only=True)
    information_files = InformationFilesSerializer(many=True, read_only=True)

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
    
    information_gallery = InformationGallerySerializer(many=True, read_only=True)
    information_files = InformationFilesSerializer(many=True, read_only=True)

    class Meta:
        model = Information
        fields = '__all__'

class IntegerListField(serializers.ListField):
    """ Handles Many-to-Many fields in form-data correctly (e.g., '[2,3]', '2,3'). """

    def to_internal_value(self, data):
        if data is None or data == "":
            return []

        if isinstance(data, list):  
            return [int(i) for i in data if str(i).isdigit()]  # Convert to integers
        
        if isinstance(data, str):  
            try:
                clean_data = data.strip("[]").replace(" ", "")  # Remove brackets & spaces

                if "," in clean_data:
                    return [int(x) for x in clean_data.split(',') if x.isdigit()]

                return [int(clean_data)] if clean_data.isdigit() else []

            except ValueError:
                raise serializers.ValidationError("Invalid format. Expected comma-separated integers.")

        return super().to_internal_value(data)



class InformationWriteSerializers(serializers.ModelSerializer):
    """ Handles Many-to-Many fields and file/image uploads """

    # Using IntegerListField for Many-to-Many relationships (comma-separated values)
    level = IntegerListField(required=False)
    sublevel = IntegerListField(required=False)
    course = IntegerListField(required=False)
    affiliation = IntegerListField(required=False)
    district = IntegerListField(required=False)
    college = IntegerListField(required=False)
    faculty = IntegerListField(required=False)
    information_tagging = IntegerListField(required=False)
    information_category = IntegerListField(required=False)

    information_gallery = serializers.SerializerMethodField()
    information_files = serializers.SerializerMethodField()

    class Meta:
        model = Information
        fields = '__all__'

    def get_information_gallery(self, obj):
        return [img.image.url for img in obj.information_gallery.all()]

    def get_information_files(self, obj):
        return [file.file.url for file in obj.information_files.all()]

    def extract_images_and_files(self):
        """ Extract multiple images and files from request.FILES """
        request = self.context.get('request')
        images_data, files_data = [], []

        if request and hasattr(request, 'FILES'):
            for key, file in request.FILES.items():
                if key.startswith('information_gallery['):
                    images_data.append(file)
                elif key.startswith('information_files['):  
                    files_data.append(file)

        return images_data, files_data

    @transaction.atomic
    def create(self, validated_data):
        """ Handles Many-to-Many relationships and image/file uploads """

        # Extract Many-to-Many fields
        many_to_many_fields = [
            "level", "sublevel", "course", "affiliation", "district",
            "college", "faculty", "information_tagging", "information_category"
        ]
        
        m2m_data = {field: validated_data.pop(field, None) for field in many_to_many_fields}

        # Extract images & files
        images_data, files_data = self.extract_images_and_files()

        # Create Information instance
        information = Information.objects.create(**validated_data)

        # Assign Many-to-Many relationships only if data is provided
        for field, ids in m2m_data.items():
            if ids is not None:
                getattr(information, field).set(ids)

        # Save images and files
        for image_file in images_data:
            InformationGallery.objects.create(information=information, image=image_file)

        for file_item in files_data:
            InformationFiles.objects.create(information=information, file=file_item)

        return information

    @transaction.atomic
    def update(self, instance, validated_data):
        """Handles updates for Many-to-Many relationships, file uploads, and form-data parsing."""

        # Extract Many-to-Many fields
        many_to_many_fields = [
            "level", "sublevel", "course", "affiliation", "district",
            "college", "faculty", "information_tagging", "information_category"
        ]
        
        m2m_data = {field: validated_data.pop(field, None) for field in many_to_many_fields}

        # Extract images & files
        images_data, files_data = self.extract_images_and_files()

        # Update instance fields
        instance = super().update(instance, validated_data)

        # Update Many-to-Many relationships only if new data is provided
        for field, ids in m2m_data.items():
            if ids is not None:
                getattr(instance, field).set(ids)

        # Add new images and files if provided
        for image_file in images_data:
            InformationGallery.objects.create(information=instance, image=image_file)

        for file_item in files_data:
            InformationFiles.objects.create(information=instance, file=file_item)

        return instance
