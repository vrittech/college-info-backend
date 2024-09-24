from rest_framework import serializers
from ..models import College

class CollegeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class CollegeRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class CollegeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'