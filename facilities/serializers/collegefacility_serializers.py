from rest_framework import serializers
from ..models import CollegeFacility, Facility
from collegemanagement.models import College

class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name','slug']
        ref_name = 'CollegeFacilitySerializers'
        
class FacilitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name']
        ref_name = 'CollegeFacilitySerializers'

class CollegeFacilityListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    facility = FacilitySerializers(read_only=True)
    class Meta:
        model = CollegeFacility
        fields = '__all__'
class CollegeFacilityRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    facility = FacilitySerializers(read_only=True)
    class Meta:
        model = CollegeFacility
        fields = '__all__'



class CollegeFacilityWriteSerializers(serializers.ModelSerializer):
    facility = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = CollegeFacility
        fields = ['college', 'facility']

    def validate(self, data):
        if not data.get("college"):
            raise serializers.ValidationError({"college": "This field is required."})
        if not data.get("facility") or not isinstance(data.get("facility"), list):
            raise serializers.ValidationError({"facility": "This field must be a list of facility IDs."})
        return data

    def create(self, validated_data):
        college = validated_data.get('college')
        facility_ids = validated_data.get('facility')
        
        # Create multiple CollegeFacility instances
        college_facilities = [
            CollegeFacility(college=college, facility_id=facility_id)
            for facility_id in facility_ids
        ]
        CollegeFacility.objects.bulk_create(college_facilities)
        
        # Fetch the created facilities to return
        facilities = Facility.objects.filter(id__in=facility_ids)

        return {"college": college, "facility": facilities}
    
    def update(self, instance, validated_data):
        college = validated_data.get('college', instance.college)
        facility_ids = validated_data.get('facility', [])

        # First, remove existing facilities related to this college (if necessary)
        CollegeFacility.objects.filter(college=college).delete()

        # Create or update multiple CollegeFacility instances
        college_facilities = [
            CollegeFacility(college=college, facility_id=facility_id)
            for facility_id in facility_ids
        ]
        CollegeFacility.objects.bulk_create(college_facilities)

        # Fetch the updated facilities to return
        facilities = Facility.objects.filter(id__in=facility_ids)

        return {"college": college, "facility": facilities}


    def to_representation(self, instance):
        """Modify response format"""
        return {
            "college": instance["college"].id if isinstance(instance, dict) else instance.college.id,
            "facility": FacilitySerializers(instance["facility"], many=True).data if isinstance(instance, dict) else FacilitySerializers(instance.facility, many=True).data
        }

