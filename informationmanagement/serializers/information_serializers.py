from rest_framework import serializers
from django.db import transaction

from ..models import Information, Level, SubLevel, Course, Affiliation, District, College, Faculty, InformationTagging, InformationCategory, InformationGallery

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
    Serializer for handling Many-to-Many fields as comma-separated values
    and handling binary image uploads in form-data.
    """

    # Expecting image uploads as binary files in form-data
    image = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Information
        fields = '__all__'

    def parse_comma_separated_values(self, field_name):
        """
        Parses comma-separated values (e.g., "1,2,3") from form-data into a list of integers.
        """
        field_value = self.initial_data.get(field_name, "")
        if field_value:
            try:
                return [int(pk.strip()) for pk in field_value.split(",") if pk.strip()]
            except ValueError:
                raise serializers.ValidationError({field_name: "Must be a comma-separated list of integers."})
        return []

    @transaction.atomic
    def create(self, validated_data):
        """
        Handles creation of Information instance with Many-to-Many fields and binary image uploads.
        """
        # Extract Many-to-Many relationships from form-data (comma-separated values)
        level_ids = self.parse_comma_separated_values('level')
        sublevel_ids = self.parse_comma_separated_values('sublevel')
        course_ids = self.parse_comma_separated_values('course')
        affiliation_ids = self.parse_comma_separated_values('affiliation')
        district_ids = self.parse_comma_separated_values('district')
        college_ids = self.parse_comma_separated_values('college')
        faculty_ids = self.parse_comma_separated_values('faculty')
        information_tagging_ids = self.parse_comma_separated_values('information_tagging')
        information_category_ids = self.parse_comma_separated_values('information_category')

        # Extract images from validated data
        images = validated_data.pop('image', [])

        # Create the Information instance
        information = Information.objects.create(**validated_data)

        # Assign Many-to-Many relationships
        information.level.set(level_ids)
        information.sublevel.set(sublevel_ids)
        information.course.set(course_ids)
        information.affiliation.set(affiliation_ids)
        information.district.set(district_ids)
        information.college.set(college_ids)
        information.faculty.set(faculty_ids)
        information.information_tagging.set(information_tagging_ids)
        information.information_category.set(information_category_ids)

        # Save image uploads
        for img in images:
            InformationGallery.objects.create(information=information, image=img)

        return information

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Handles updating of Information instance with Many-to-Many fields and binary image uploads.
        """
        # Extract Many-to-Many relationships from form-data (comma-separated values)
        level_ids = self.parse_comma_separated_values('level')
        sublevel_ids = self.parse_comma_separated_values('sublevel')
        course_ids = self.parse_comma_separated_values('course')
        affiliation_ids = self.parse_comma_separated_values('affiliation')
        district_ids = self.parse_comma_separated_values('district')
        college_ids = self.parse_comma_separated_values('college')
        faculty_ids = self.parse_comma_separated_values('faculty')
        information_tagging_ids = self.parse_comma_separated_values('information_tagging')
        information_category_ids = self.parse_comma_separated_values('information_category')

        # Extract images from validated data
        images = validated_data.pop('image', [])

        # Update instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Many-to-Many relationships
        instance.level.set(level_ids)
        instance.sublevel.set(sublevel_ids)
        instance.course.set(course_ids)
        instance.affiliation.set(affiliation_ids)
        instance.district.set(district_ids)
        instance.college.set(college_ids)
        instance.faculty.set(faculty_ids)
        instance.information_tagging.set(information_tagging_ids)
        instance.information_category.set(information_category_ids)

        # Save new image uploads (append to existing images)
        for img in images:
            InformationGallery.objects.create(information=instance, image=img)

        return instance

# {
#   "title": "Sample Information",
#   "publish_date": "2024-12-01T00:00:00Z",
#   "active_period_start": "2024-12-01",
#   "active_period_end": "2024-12-31",
#   "level": [1, 2],
#   "sublevel": [3],
#   "course": [4, 5],
#   "affiliation": [6],
#   "district": [7],
#   "college": [8],
#   "faculty": [9],
#   "information_tagging": [10],
#   "information_category": [11],
#   "image": [12, 13],
#   "short_description": "Short description here",
#   "description": "Detailed description here"
# }
