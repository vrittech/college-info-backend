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
    # Nested serializers for ForeignKey fields
    district = DistrictSerializer()  # Include full object instead of just ID
    affiliated = AffiliationSerializer()  # Include full object instead of just ID
    college_type = CollegeTypeSerializer()  # Include full object instead of just ID

    # Nested serializers for ManyToMany fields
    discipline = DisciplineSerializer(many=True)  # Include full objects for many-to-many relationships
    social_media = SocialMediaSerializer(many=True)  # Include full objects for many-to-many relationships
    facilities = FacilitySerializer(many=True)  # Include full objects for many-to-many relationships

    class Meta:
        model = College
        fields = '__all__'

    # Custom method to handle creation of College instances
    def create(self, validated_data):
        district_data = validated_data.pop('district')
        affiliated_data = validated_data.pop('affiliated')
        college_type_data = validated_data.pop('college_type')
        discipline_data = validated_data.pop('discipline')
        social_media_data = validated_data.pop('social_media')
        facilities_data = validated_data.pop('facilities')

        # Create related objects first
        district = District.objects.create(**district_data)
        affiliated = Affiliation.objects.create(**affiliated_data)
        college_type = CollegeType.objects.create(**college_type_data)

        # Create College instance
        college = College.objects.create(
            district=district, affiliated=affiliated, college_type=college_type, **validated_data
        )

        # Handle ManyToMany relationships by adding related objects
        for discipline in discipline_data:
            college.discipline.add(Discipline.objects.create(**discipline))

        for social in social_media_data:
            college.social_media.add(SocialMedia.objects.create(**social))

        for facility in facilities_data:
            college.facilities.add(Facility.objects.create(**facility))

        return college

    # Custom method to handle updating of College instances
    def update(self, instance, validated_data):
        district_data = validated_data.pop('district', None)
        affiliated_data = validated_data.pop('affiliated', None)
        college_type_data = validated_data.pop('college_type', None)
        discipline_data = validated_data.pop('discipline', None)
        social_media_data = validated_data.pop('social_media', None)
        facilities_data = validated_data.pop('facilities', None)

        # Update ForeignKey fields if new data is provided
        if district_data:
            for attr, value in district_data.items():
                setattr(instance.district, attr, value)
            instance.district.save()

        if affiliated_data:
            for attr, value in affiliated_data.items():
                setattr(instance.affiliated, attr, value)
            instance.affiliated.save()

        if college_type_data:
            for attr, value in college_type_data.items():
                setattr(instance.college_type, attr, value)
            instance.college_type.save()

        # Add new ManyToMany relationships and remove items marked for deletion
        if discipline_data:
            # Adding new disciplines (if provided)
            current_discipline_ids = {d.id for d in instance.discipline.all()}
            new_discipline_ids = {d['id'] for d in discipline_data}

            # Add new disciplines (without duplicates)
            for discipline in discipline_data:
                if discipline['id'] not in current_discipline_ids:
                    instance.discipline.add(Discipline.objects.get(id=discipline['id']))

            # Remove disciplines that are no longer part of the request (if any)
            for discipline in instance.discipline.all():
                if discipline.id not in new_discipline_ids:
                    instance.discipline.remove(discipline)

        if social_media_data:
            # Adding new social media links (if provided)
            current_social_media_ids = {sm.id for sm in instance.social_media.all()}
            new_social_media_ids = {sm['id'] for sm in social_media_data}

            # Add new social media (without duplicates)
            for social_media in social_media_data:
                if social_media['id'] not in current_social_media_ids:
                    instance.social_media.add(SocialMedia.objects.get(id=social_media['id']))

            # Remove social media that are no longer part of the request (if any)
            for social_media in instance.social_media.all():
                if social_media.id not in new_social_media_ids:
                    instance.social_media.remove(social_media)

        if facilities_data:
            # Adding new facilities (if provided)
            current_facilities_ids = {f.id for f in instance.facilities.all()}
            new_facilities_ids = {f['id'] for f in facilities_data}

            # Add new facilities (without duplicates)
            for facility in facilities_data:
                if facility['id'] not in current_facilities_ids:
                    instance.facilities.add(Facility.objects.get(id=facility['id']))

            # Remove facilities that are no longer part of the request (if any)
            for facility in instance.facilities.all():
                if facility.id not in new_facilities_ids:
                    instance.facilities.remove(facility)

        # Update the other fields in the College model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

