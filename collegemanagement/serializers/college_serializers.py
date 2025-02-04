from rest_framework import serializers
from ..models import College, District, Affiliation, CollegeType, Discipline, SocialMedia, Facility

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
    
    class Meta:
        model = College
        fields = '__all__'
