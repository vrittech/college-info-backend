from rest_framework import serializers
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
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all(), many=True, required=False)
    sublevel = serializers.PrimaryKeyRelatedField(queryset=SubLevel.objects.all(), many=True, required=False)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, required=False)
    affiliation = serializers.PrimaryKeyRelatedField(queryset=Affiliation.objects.all(), many=True, required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), many=True, required=False)
    college = serializers.PrimaryKeyRelatedField(queryset=College.objects.all(), many=True, required=False)
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(), many=True, required=False)
    information_tagging = serializers.PrimaryKeyRelatedField(queryset=InformationTagging.objects.all(), many=True, required=False)
    information_category = serializers.PrimaryKeyRelatedField(queryset=InformationCategory.objects.all(), many=True, required=False)
    image = serializers.PrimaryKeyRelatedField(queryset=InformationGallery.objects.all(), many=True, required=False)

    class Meta:
        model = Information
        fields = '__all__'

    def create(self, validated_data):
        """
        Handles creation of Information instance with related objects based on provided ids.
        """
        # Extract the related fields (ManyToMany)
        level_ids = validated_data.pop('level', [])
        sublevel_ids = validated_data.pop('sublevel', [])
        course_ids = validated_data.pop('course', [])
        affiliation_ids = validated_data.pop('affiliation', [])
        district_ids = validated_data.pop('district', [])
        college_ids = validated_data.pop('college', [])
        faculty_ids = validated_data.pop('faculty', [])
        information_tagging_ids = validated_data.pop('information_tagging', [])
        information_category_ids = validated_data.pop('information_category', [])
        image_ids = validated_data.pop('image', [])

        # Create the Information instance first
        information = Information.objects.create(**validated_data)

        # Assign ManyToMany relationships
        if level_ids:
            information.level.set(level_ids)
        if sublevel_ids:
            information.sublevel.set(sublevel_ids)
        if course_ids:
            information.course.set(course_ids)
        if affiliation_ids:
            information.affiliation.set(affiliation_ids)
        if district_ids:
            information.district.set(district_ids)
        if college_ids:
            information.college.set(college_ids)
        if faculty_ids:
            information.faculty.set(faculty_ids)
        if information_tagging_ids:
            information.information_tagging.set(information_tagging_ids)
        if information_category_ids:
            information.information_category.set(information_category_ids)
        if image_ids:
            information.image.set(image_ids)

        return information

    def update(self, instance, validated_data):
        """
        Handles the update of Information instance with related objects based on provided ids.
        """
        # Extract the related fields (ManyToMany)
        level_ids = validated_data.pop('level', [])
        sublevel_ids = validated_data.pop('sublevel', [])
        course_ids = validated_data.pop('course', [])
        affiliation_ids = validated_data.pop('affiliation', [])
        district_ids = validated_data.pop('district', [])
        college_ids = validated_data.pop('college', [])
        faculty_ids = validated_data.pop('faculty', [])
        information_tagging_ids = validated_data.pop('information_tagging', [])
        information_category_ids = validated_data.pop('information_category', [])
        image_ids = validated_data.pop('image', [])

        # Update the fields of the Information instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ManyToMany relationships
        if level_ids:
            instance.level.set(level_ids)
        if sublevel_ids:
            instance.sublevel.set(sublevel_ids)
        if course_ids:
            instance.course.set(course_ids)
        if affiliation_ids:
            instance.affiliation.set(affiliation_ids)
        if district_ids:
            instance.district.set(district_ids)
        if college_ids:
            instance.college.set(college_ids)
        if faculty_ids:
            instance.faculty.set(faculty_ids)
        if information_tagging_ids:
            instance.information_tagging.set(information_tagging_ids)
        if information_category_ids:
            instance.information_category.set(information_category_ids)
        if image_ids:
            instance.image.set(image_ids)

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
