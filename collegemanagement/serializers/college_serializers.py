from rest_framework import serializers
from ..models import College, District, Affiliation, CollegeType, Discipline
from socialmedia.models import SocialMedia,CollegeSocialMedia
from formprogress.models import FormStepProgress
import ast

def str_to_list(data, value_to_convert):
    try:
        mutable_data = data.dict()  # Convert to dictionary if possible
    except AttributeError:
        mutable_data = data  # Already a dictionary

    value_to_convert_data = mutable_data.get(value_to_convert)

    # If it's already a list, return as is
    if isinstance(value_to_convert_data, list):
        return mutable_data

    # Handle binary or file data (leave as is)
    if isinstance(value_to_convert_data, bytes):
        return mutable_data

    # If it's an int, float, or bool, wrap it in a list
    if isinstance(value_to_convert_data, (int, float, bool)):
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

    # If it's None, convert to an empty list
    if value_to_convert_data is None:
        mutable_data[value_to_convert] = []
        return mutable_data

    # Handle comma-separated values (e.g., "4,5," -> [4, 5])
    if isinstance(value_to_convert_data, str) and "," in value_to_convert_data:
        parsed_list = [
            item.strip() for item in value_to_convert_data.split(",") if item.strip().isdigit()
        ]  # ✅ Remove empty strings and ensure only digits

        # Convert to integers
        mutable_data[value_to_convert] = [int(item) for item in parsed_list]
        return mutable_data

    # If it's a string, try parsing it as a list
    try:
        parsed_value = ast.literal_eval(value_to_convert_data)

        # Ensure parsed result is a list
        if isinstance(parsed_value, list):
            mutable_data[value_to_convert] = parsed_value
        else:
            # Convert string (that is not a list) into a single-item list
            mutable_data[value_to_convert] = [value_to_convert_data]

        return mutable_data

    except (ValueError, SyntaxError):
        # If parsing fails, wrap it in a list instead
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

# Nested serializer for District
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']

# Nested serializer for Affiliation
class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id','slug', 'name', 'established_year','address']

# Nested serializer for CollegeType
class FormStepProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormStepProgress
        fields = '__all__'
        
class CollegeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeType
        fields = '__all__'

# Nested serializer for Discipline
class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'
        ref_name = 'Disciplines'

# Nested serializer for SocialMedia
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeSocialMedia
        fields = '__all__'

# # Nested serializer for Facility
# class FacilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Facility
#         fields = ['id', 'name','is_show']


# Serializer for listing college details (basic view)
class CollegeListSerializers(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)  # Nested object for related model
    affiliated = AffiliationSerializer(read_only=True)  # Nested object for related model
    college_type = CollegeTypeSerializer(read_only=True)  # Nested object for related model
    discipline = DisciplineSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    social_media = SocialMediaSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    # facilities = FacilitySerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    profile_completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = '__all__'

    def get_profile_completion_percentage(self, obj):
        return obj.get_profile_completion_percentage

# Serializer for retrieving complete college details (detailed view)
class CollegeRetrieveSerializers(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)  # Nested object for related model
    affiliated = AffiliationSerializer(read_only=True)  # Nested object for related model
    college_type = CollegeTypeSerializer(read_only=True)  # Nested object for related model
    discipline = DisciplineSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    social_media = SocialMediaSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    profile_completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = '__all__'

    def get_profile_completion_percentage(self, obj):
        return obj.get_profile_completion_percentage


# Serializer for creating/updating college details (with nested objects for foreign keys and many-to-many)
# Serializer for College model
class CollegeWriteSerializers(serializers.ModelSerializer):

    class Meta:
        model = College
        fields = '__all__'
        
    def to_internal_value(self, data):
            """Convert certification input from string to list using str_to_list."""
            data = str_to_list(data, 'discipline')  # Convert string to list for certification
            # data = str_to_list(data, 'facilities')  
            return super().to_internal_value(data)

    def create(self, validated_data):
        """Handles creating a college and returns full objects in response."""
        request = self.context.get("request")

        # ✅ Convert and clean discipline_ids
        request_data = str_to_list(request.data, "discipline")
        discipline_ids = request_data.get("discipline", [])

        # ✅ Remove ManyToMany fields from validated_data
        validated_data.pop("discipline", None)

        # ✅ Create College instance
        college = College.objects.create(**validated_data)

        # ✅ Set ManyToMany relationships, ensuring only valid IDs are used
        if discipline_ids:
            college.discipline.set(Discipline.objects.filter(id__in=discipline_ids))

        return college

    def update(self, instance, validated_data):
        """Handles updating a college and returns full objects in response."""
        request = self.context.get("request")

        # ✅ Ensure discipline and facilities are properly formatted
        request_data = str_to_list(request.data, "discipline")
        # request_data = str_to_list(request_data, "facilities")

        discipline_ids = request_data.get("discipline", [])
        # facilities_ids = request_data.get("facilities", [])

        # ✅ Exclude ManyToMany fields from direct assignment
        many_to_many_fields = {"discipline"}

        for attr, value in validated_data.items():
            if attr not in many_to_many_fields:  # ✅ Skip ManyToMany fields
                setattr(instance, attr, value)
        instance.save()

        # ✅ Update ManyToMany relationships separately
        if discipline_ids:
            instance.discipline.set(Discipline.objects.filter(id__in=discipline_ids))

        # if facilities_ids:
        #     instance.facilities.set(Facility.objects.filter(id__in=facilities_ids))

        return instance






    def to_representation(self, instance):
        """Customize the response to include full objects for related fields."""
        response = super().to_representation(instance)
        # response["slug"] = instance.slug

        # Replace IDs with full nested objects for foreign key fields
        response["district"] = DistrictSerializer(instance.district).data
        response["affiliated"] = AffiliationSerializer(instance.affiliated).data
        response["college_type"] = CollegeTypeSerializer(instance.college_type).data
        response["step_counter"] = (
            FormStepProgressSerializer(instance.step_counter).data if instance.step_counter else None
        )

        # Replace IDs with full nested objects for many-to-many fields
        response["discipline"] = DisciplineSerializer(instance.discipline.all(), many=True).data
        # response["social_media"] = SocialMediaSerializer(instance.social_media.all(), many=True).data
        # response["facilities"] = FacilitySerializer(instance.facilities.all(), many=True).data

        return response


class CollegeAdminWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id','name','affiliated','college_type','phone_number']