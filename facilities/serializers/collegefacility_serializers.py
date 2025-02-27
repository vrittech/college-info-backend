from rest_framework import serializers
from ..models import CollegeFacility
from collegemanagement.models import College

class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name','slug']
        ref_name = 'CollegeFacilitySerializers'

class CollegeFacilityListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    class Meta:
        model = CollegeFacility
        fields = '__all__'

class CollegeFacilityRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    class Meta:
        model = CollegeFacility
        fields = '__all__'

class CollegeFacilityWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeFacility
        fields = '__all__'