from rest_framework import serializers
from ..models import CoursesAndFees
from collegemanagement.models import College
from coursemanagement.models import Course
from duration.models import Duration
from affiliation.models import Affiliation


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        ref_name = 'course_affiliation'
        fields = ['id','name','slug']
        

class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        ref_name = 'course'
        fields = ['id','name']
        
class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['slug','id','name']
        
class CourseSerializers(serializers.ModelSerializer):
    affiliation = AffiliationSerializer(read_only=True)
    duration = DurationSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ['slug','id','name','affiliation','duration']
         
        
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
    college = CollegeSerializers(read_only=True)
    course = CourseSerializers(read_only=True)
    class Meta:
        model = CoursesAndFees
        fields = '__all__'