from rest_framework import serializers
from ..models import Inquiry
from coursemanagement.models import Course
from collegemanagement.models import College


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name','slug']
        
class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id','name','slug']
        
class InquiryListSerializers(serializers.ModelSerializer):
    courses = CourseSerializers(read_only=True,many=True)
    colleges = CourseSerializers(read_only=True,many=True)
    class Meta:
        model = Inquiry
        fields = '__all__'

class InquiryRetrieveSerializers(serializers.ModelSerializer):
    courses = CourseSerializers(read_only=True,many=True)
    colleges = CourseSerializers(read_only=True,many=True)
    class Meta:
        model = Inquiry
        fields = '__all__'

class InquiryWriteSerializers(serializers.ModelSerializer):
    courses = CourseSerializers(read_only=True,many=True)
    colleges = CourseSerializers(read_only=True,many=True)
    class Meta:
        model = Inquiry
        fields = '__all__'