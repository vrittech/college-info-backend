from rest_framework import serializers
from ..models import CoursesAndFees
from collegemanagement.models import College
from coursemanagement.models import Course

class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'
        
class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
        
class CoursesAndFeesListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    course = CourseSerializers(read_only=True)
    class Meta:
        model = CoursesAndFees
        fields = '__all__'

class CoursesAndFeesRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    course = CourseSerializers(read_only=True)
    class Meta:
        model = CoursesAndFees
        fields = '__all__'

class CoursesAndFeesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoursesAndFees
        fields = '__all__'