from rest_framework import serializers
from ..models import Semester

class SemesterListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class SemesterRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class SemesterWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'