from rest_framework import serializers
from ..models import College, District, Affiliation, CollegeType, Discipline, Facility
from socialmedia.models import SocialMedia,CollegeSocialMedia
from formprogress.models import FormStepProgress
import ast


def str_to_list(data,value_to_convert):
    try:
        mutable_data = data.dict()
    except Exception:
        mutable_data = data
    value_to_convert_data = mutable_data[value_to_convert]
    if isinstance(value_to_convert_data,list):# type(value_to_convert_data) == list:

        return mutable_data
    try:
        variations = ast.literal_eval(value_to_convert_data)
        mutable_data[value_to_convert] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({f'{value_to_convert}': str(e)}) from e
    
# Nested serializer for District
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']

# Nested serializer for Affiliation
class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'name', 'established_year','address']

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

# Nested serializer for Facility
class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


# Serializer for listing college details (basic view)
class CollegeListSerializers(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)  # Nested object for related model
    affiliated = AffiliationSerializer(read_only=True)  # Nested object for related model
    college_type = CollegeTypeSerializer(read_only=True)  # Nested object for related model
    discipline = DisciplineSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    social_media = SocialMediaSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    facilities = FacilitySerializer(many=True,read_only=True)  # Nested objects for ManyToMany

    class Meta:
        model = College
        fields = '__all__'


# Serializer for retrieving complete college details (detailed view)
class CollegeRetrieveSerializers(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)  # Nested object for related model
    affiliated = AffiliationSerializer(read_only=True)  # Nested object for related model
    college_type = CollegeTypeSerializer(read_only=True)  # Nested object for related model
    discipline = DisciplineSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    social_media = SocialMediaSerializer(many=True,read_only=True)  # Nested objects for ManyToMany
    facilities = FacilitySerializer(many=True,read_only=True)  # Nested objects for ManyToMany

    class Meta:
        model = College
        fields = '__all__'


# Serializer for creating/updating college details (with nested objects for foreign keys and many-to-many)
# Serializer for College model
class CollegeWriteSerializers(serializers.ModelSerializer):
    # ForeignKey fields
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    affiliated = serializers.PrimaryKeyRelatedField(queryset=Affiliation.objects.all())
    college_type = serializers.PrimaryKeyRelatedField(queryset=CollegeType.objects.all())
    step_counter = serializers.PrimaryKeyRelatedField(queryset=FormStepProgress.objects.all(), required=False, allow_null=True)

    # ManyToMany fields
    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all(), many=True)
    social_media = SocialMediaSerializer(many=True, required=False)
    facilities = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all(), many=True, required=False)
    
    def to_internal_value(self, data):
        """Converts stringified social media JSON into a list before validation."""
        if data.get('social_media'):
            data['social_media'] = str_to_list(data, 'social_media')  # Convert if stringified
        return super().to_internal_value(data)

    class Meta:
        model = College
        fields = '__all__'

    def create(self, validated_data):
        """Handles creating a college and returns full objects in response."""
        request = self.context.get("request")

        # Extract ManyToMany relationships from the request
        discipline_ids = request.data.get("discipline", [])
        social_media_data = request.data.get("social_media", None) 
        facilities_ids = request.data.get("facilities", [])

        # Remove ManyToMany fields from validated_data
        validated_data.pop("discipline", None)
        validated_data.pop("social_media", None)
        validated_data.pop("facilities", None)

        # Create College instance
        college = College.objects.create(**validated_data)

        # Set ManyToMany relationships
        if discipline_ids:
            college.discipline.set(Discipline.objects.filter(id__in=discipline_ids))
        if facilities_ids:
            college.facilities.set(Facility.objects.filter(id__in=facilities_ids))

        return college

    def update(self, instance, validated_data):
        """Handles updating a college and returns full objects in response."""
        request = self.context.get("request")

        # Extract ManyToMany relationships from the request
        discipline_ids = request.data.get("discipline", None)
        social_media_data = request.data.get("social_media", None)
        facilities_ids = request.data.get("facilities", None)

        # Remove ManyToMany fields from validated_data
        validated_data.pop("discipline", None)
        # validated_data.pop("social_media", None)
        validated_data.pop("facilities", None)

        # Update ForeignKey fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ManyToMany relationships
        if discipline_ids is not None:
            instance.discipline.set(Discipline.objects.filter(id__in=discipline_ids))
        # if social_media_ids is not None:
        #     instance.social_media.set(SocialMedia.objects.filter(id__in=social_media_ids))
        if facilities_ids is not None:
            instance.facilities.set(Facility.objects.filter(id__in=facilities_ids))

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
        response["facilities"] = FacilitySerializer(instance.facilities.all(), many=True).data

        return response


class CollegeAdminWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id','name','affiliated','college_type','phone_number']