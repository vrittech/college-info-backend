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
    class Meta:
        model = CollegeFacility
        fields = '__all__'
    
    def validate(self, data):
        if not data.get("college"):
            raise serializers.ValidationError({"college": "This field is required."})
        if not data.get("facility"):
            raise serializers.ValidationError({"facility": "This field is required."})
        return data
