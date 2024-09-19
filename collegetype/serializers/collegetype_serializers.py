from rest_framework import serializers
from ..models import CollegeType

class CollegeTypeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeType
        fields = '__all__'

class CollegeTypeRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeType
        fields = '__all__'

class CollegeTypeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeType
        fields = '__all__'