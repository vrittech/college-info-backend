from rest_framework import serializers
from ..models import Facility

class FacilityListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'

class FacilityRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'

class FacilityWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'