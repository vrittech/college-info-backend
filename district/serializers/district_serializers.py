from rest_framework import serializers
from ..models import District

class DistrictListSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class DistrictRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class DistrictWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'