from rest_framework import serializers
from ..models import CourseCurriculumFile

class CourseCurriculumFileListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCurriculumFile
        fields = '__all__'

class CourseCurriculumFileRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCurriculumFile
        fields = '__all__'

class CourseCurriculumFileWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCurriculumFile
        fields = '__all__'