from rest_framework import serializers
from ..models import College, District, Affiliation, CollegeType, Discipline, SocialMedia, Facility
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
        fields = '__all__'

# Nested serializer for Affiliation
class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

# Nested serializer for CollegeType
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
        model = SocialMedia
        fields = '__all__'

# Nested serializer for Facility
class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


# Serializer for listing college details (basic view)
class CollegeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


# Serializer for retrieving complete college details (detailed view)
class CollegeRetrieveSerializers(serializers.ModelSerializer):
    district = DistrictSerializer()  # Nested object for related model
    affiliated = AffiliationSerializer()  # Nested object for related model
    college_type = CollegeTypeSerializer()  # Nested object for related model
    discipline = DisciplineSerializer(many=True)  # Nested objects for ManyToMany
    social_media = SocialMediaSerializer(many=True)  # Nested objects for ManyToMany
    facilities = FacilitySerializer(many=True)  # Nested objects for ManyToMany

    class Meta:
        model = College
        fields = '__all__'


# Serializer for creating/updating college details (with nested objects for foreign keys and many-to-many)
class CollegeWriteSerializers(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField to accept only IDs
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    affiliated = serializers.PrimaryKeyRelatedField(queryset=Affiliation.objects.all())
    college_type = serializers.PrimaryKeyRelatedField(queryset=CollegeType.objects.all())

    discipline = serializers.PrimaryKeyRelatedField(queryset=Discipline.objects.all(), many=True)
    social_media = serializers.PrimaryKeyRelatedField(queryset=SocialMedia.objects.all(), many=True)
    facilities = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all(), many=True)
    def to_internal_value(self, data):
        if data.get('packages'):
            data = str_to_list(data,'packages')
            return super().to_internal_value(data)
        return super().to_internal_value(data)

    class Meta:
        model = College
        fields = '__all__'
        
    def create(self, validated_data):
        discipline_ids = validated_data.pop('discipline', [])
        social_media_ids = validated_data.pop('social_media', [])
        facilities_ids = validated_data.pop('facilities', [])

        # Create College instance with ForeignKey relationships
        college = College.objects.create(**validated_data)

        # Add ManyToMany relationships using IDs
        college.discipline.set(discipline_ids)
        college.social_media.set(social_media_ids)
        college.facilities.set(facilities_ids)

        return college

    def update(self, instance, validated_data):
        discipline_ids = validated_data.pop('discipline', None)
        social_media_ids = validated_data.pop('social_media', None)
        facilities_ids = validated_data.pop('facilities', None)

        # Update ForeignKey relationships
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ManyToMany relationships if provided
        if discipline_ids is not None:
            instance.discipline.set(discipline_ids)
        if social_media_ids is not None:
            instance.social_media.set(social_media_ids)
        if facilities_ids is not None:
            instance.facilities.set(facilities_ids)

        return instance
