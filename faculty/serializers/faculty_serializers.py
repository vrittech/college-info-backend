from rest_framework import serializers
from ..models import Faculty

class FacultyListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class FacultyRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class FacultyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'