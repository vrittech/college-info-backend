from rest_framework import serializers
from ..models import Course

class CourseListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'