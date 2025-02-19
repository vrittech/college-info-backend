from rest_framework import serializers
from django.db import transaction
import ast

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
        if isinstance(data, list):  
            return [int(i) for i in data]  # Already a list, convert values to integers
        
        if isinstance(data, str):  
            try:
                clean_data = data.strip("[]").replace(" ", "")  # Remove brackets & spaces

                # If string is like "2,3", split and convert to list
                if "," in clean_data:
                    return list(map(int, clean_data.split(',')))

                # If single number, return as list
                return [int(clean_data)]  

            except ValueError:
                raise serializers.ValidationError("Invalid format. Expected comma-separated integers.")

        return super().to_internal_value(data)

class InformationWriteSerializers(serializers.ModelSerializer):
    """ Handles Many-to-Many fields and file/image uploads """

    level = IntegerListField(child=serializers.IntegerField(), required=False)
    sublevel = IntegerListField(child=serializers.IntegerField(), required=False)
    course = IntegerListField(child=serializers.IntegerField(), required=False)
    affiliation = IntegerListField(child=serializers.IntegerField(), required=False)
    district = IntegerListField(child=serializers.IntegerField(), required=False)
    college = IntegerListField(child=serializers.IntegerField(), required=False)
    faculty = IntegerListField(child=serializers.IntegerField(), required=False)
    information_tagging = IntegerListField(child=serializers.IntegerField(), required=False)
    information_category = IntegerListField(child=serializers.IntegerField(), required=False)

    # Read-only for returned images and files
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
        """ Extract multiple images and files from `image[0]`, `image[1]` keys in request.FILES """
        images_data, files_data = [], []
        request = self.context.get('request')

        if request and hasattr(request, 'FILES'):
            for key, file in request.FILES.items():
                if key.startswith('information_gallery['):  # Accept multiple images as `image[0]`, `image[1]`
                    images_data.append(file)
                elif key.startswith('informations_files['):  # Accept multiple files as `file[0]`, `file[1]`
                    files_data.append(file)

        return images_data, files_data

    @transaction.atomic
    def create(self, validated_data):
        """ Handles Many-to-Many relationships and image/file uploads """

        # Extract Many-to-Many field IDs
        level_ids = validated_data.pop('level', [])
        sublevel_ids = validated_data.pop('sublevel', [])
        course_ids = validated_data.pop('course', [])
        affiliation_ids = validated_data.pop('affiliation', [])
        district_ids = validated_data.pop('district', [])
        college_ids = validated_data.pop('college', [])
        faculty_ids = validated_data.pop('faculty', [])
        information_tagging_ids = validated_data.pop('information_tagging', [])
        information_category_ids = validated_data.pop('information_category', [])

        # Extract images & files from request FILES
        images_data, files_data = self.extract_images_and_files()

        # Create Information instance
        information = Information.objects.create(**validated_data)

        # Assign Many-to-Many relationships
        information.level.add(*level_ids)
        information.sublevel.add(*sublevel_ids)
        information.course.add(*course_ids)
        information.affiliation.add(*affiliation_ids)
        information.district.add(*district_ids)
        information.college.add(*college_ids)
        information.faculty.add(*faculty_ids)
        information.information_tagging.add(*information_tagging_ids)
        information.information_category.add(*information_category_ids)

        # Save images to InformationGallery
        for image_file in images_data:
            InformationGallery.objects.create(information=information, image=image_file)

        # Save files to InformationFiles
        for file_item in files_data:
            InformationFiles.objects.create(information=information, file=file_item)

        return information

    @transaction.atomic
    def update(self, instance, validated_data):
        """Handles updates for Many-to-Many relationships, file uploads, and form-data parsing.
        Ensures Many-to-Many fields can be passed as comma-separated values.
        """

        request = self.context.get('request')
        images_data, files_data = [], []

        # Extract images & files from request FILES
        if request and hasattr(request, 'FILES'):
            for key, file in request.FILES.items():
                if key.startswith('information_gallery['):  # Accept multiple images as `image[0]`, `image[1]`
                    images_data.append(file)
                elif key.startswith('informations_files['):  # Accept multiple files as `file[0]`, `file[1]`
                    files_data.append(file)

        # Extract Many-to-Many fields (comma-separated values from form-data)
        many_to_many_fields = [
            "level", "sublevel", "course", "affiliation", "district",
            "college", "faculty", "information_tagging", "information_category"
        ]

        for field in many_to_many_fields:
            if field in validated_data:
                validated_data[field] = [
                    int(val.strip()) for val in validated_data[field].split(',') if val.strip().isdigit()
                ]  # Convert comma-separated values into a list of integers

        # Extract Many-to-Many field IDs
        level_ids = validated_data.pop('level', None)
        sublevel_ids = validated_data.pop('sublevel', None)
        course_ids = validated_data.pop('course', None)
        affiliation_ids = validated_data.pop('affiliation', None)
        district_ids = validated_data.pop('district', None)
        college_ids = validated_data.pop('college', None)
        faculty_ids = validated_data.pop('faculty', None)
        information_tagging_ids = validated_data.pop('information_tagging', None)
        information_category_ids = validated_data.pop('information_category', None)

        # Update instance fields only if validated_data is not empty
        if validated_data:
            instance = super().update(instance, validated_data)

        # Update Many-to-Many relationships only if new data is provided
        if level_ids is not None:
            instance.level.set(level_ids)
        if sublevel_ids is not None:
            instance.sublevel.set(sublevel_ids)
        if course_ids is not None:
            instance.course.set(course_ids)
        if affiliation_ids is not None:
            instance.affiliation.set(affiliation_ids)
        if district_ids is not None:
            instance.district.set(district_ids)
        if college_ids is not None:
            instance.college.set(college_ids)
        if faculty_ids is not None:
            instance.faculty.set(faculty_ids)
        if information_tagging_ids is not None:
            instance.information_tagging.set(information_tagging_ids)
        if information_category_ids is not None:
            instance.information_category.set(information_category_ids)

        # Only update images if new ones are provided
        if images_data:
            for image_file in images_data:
                InformationGallery.objects.create(information=instance, image=image_file)

        # Only update files if new ones are provided
        if files_data:
            for file_item in files_data:
                InformationFiles.objects.create(information=instance, file=file_item)

        return instance
