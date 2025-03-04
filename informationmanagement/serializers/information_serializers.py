from rest_framework import serializers
from django.db import transaction
import ast

from ..models import Information, Level, SubLevel, Course, Affiliation, District, College, Faculty, InformationTagging, InformationCategory, InformationGallery, InformationFiles
from rest_framework import serializers
from django.db import transaction
from informationmanagement.models import (
    Information, InformationGallery, InformationFiles
)
""" 
    This string list is used to convert string to list of integers or list of strings 
    and when frontend send list of ids in string format then we need to convert it to list of integers
    for example if frontend send '1,2,3' then we need to convert it to [1,2,3]
    or "1,2,3,4" to [1,2,3,4]
"""

def str_to_list(data, value_to_convert):
    """
    Converts a string representation of a list into an actual list if necessary.
    Ensures that single values or comma-separated values are correctly converted into lists of integers.
    """
    try:
        mutable_data = data.dict()  # Convert QueryDict to standard dict if necessary
    except Exception:
        mutable_data = data

    value_to_convert_data = mutable_data.get(value_to_convert)

    if isinstance(value_to_convert_data, list):
        return mutable_data  # If already a list, return unchanged

    # If it's a comma-separated string, convert it to a list of integers
    if isinstance(value_to_convert_data, str):
        if ',' in value_to_convert_data:
            # Split the string by commas, strip spaces, and convert each part to an integer
            mutable_data[value_to_convert] = [int(x.strip()) for x in value_to_convert_data.split(',')]
        else:
            # If it's a single value, convert it to a list of one integer
            mutable_data[value_to_convert] = [int(value_to_convert_data.strip())]
        return mutable_data

    # If it's a single item (not a list or string), wrap it in a list
    if value_to_convert_data and not isinstance(value_to_convert_data, list):
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

    try:
        variations = ast.literal_eval(value_to_convert_data)  # Convert string to list
        mutable_data[value_to_convert] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({f'{value_to_convert}': str(e)}) from e
    
    
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




class InformationWriteSerializers(serializers.ModelSerializer):
    """Handles Many-to-Many fields and file/image uploads."""

    information_gallery = InformationGallerySerializer(many=True,read_only = True)
    information_files = InformationFilesSerializer(many=True,read_only = True)

    class Meta:
        model = Information
        fields = '__all__'
    
    def to_representation(self, instance):
        attrs = super().to_representation(instance)

        # Make the gallery URLs absolute
        for item in attrs['information_gallery']:
            if item.get('image'):
                item['image'] = self.get_absolute_url(item['image'])

        # Make the file URLs absolute
        for item in attrs['information_files']:
            if item.get('file'):
                item['file'] = self.get_absolute_url(item['file'])

        return attrs

    def get_absolute_url(self, file_field):
        """
        Returns the absolute URL for a file or image field.
        """
        request = self.context.get('request')
        if not request:
            return file_field.url
        return request.build_absolute_uri(file_field.url)

    # def get_information_gallery(self, obj):
    #     return [img.image.url for img in obj.information_gallery.all()]

    # def get_information_files(self, obj):
    #     return [file.file.url for file in obj.information_files.all()]

    def to_internal_value(self, data):
        """
        Override to_internal_value to handle Many-to-Many fields.
        """
        # List of fields that need to be converted from string to list
        many_to_many_fields = [
            "level", "sublevel", "course", "affiliation", "district",
            "college", "faculty", "information_tagging", "information_category"
        ]

        # Convert each field using str_to_list
        for field in many_to_many_fields:
            if field in data:
                data = str_to_list(data, field)

        return super().to_internal_value(data)

    def extract_images_and_files(self):
        """Extract multiple images and files from request.FILES."""
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
        """Handles Many-to-Many relationships and image/file uploads."""

        # Extract Many-to-Many fields
        many_to_many_fields = [
            "level", "sublevel", "course", "affiliation", "district",
            "college", "faculty", "information_tagging", "information_category"
        ]

        m2m_data = {field: validated_data.pop(field, []) for field in many_to_many_fields}

        # Extract images & files
        images_data, files_data = self.extract_images_and_files()

        # Create Information instance
        information = Information.objects.create(**validated_data)

        # Assign Many-to-Many relationships
        for field, ids in m2m_data.items():
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
