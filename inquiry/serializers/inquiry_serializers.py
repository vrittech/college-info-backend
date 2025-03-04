from rest_framework import serializers
from ..models import Inquiry
from coursemanagement.models import Course
from collegemanagement.models import College


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        ref_name = 'CourseInquirySerializers'
        fields = ['id','name','slug','image']
        
class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        ref_name = 'CollegeInquirySerializers'
        fields = ['id','name','slug','dp_image']
        
class InquiryListSerializers(serializers.ModelSerializer):
    courses = CourseSerializers(read_only=True,many=True)
    colleges = CollegeSerializers(read_only=True,many=True)
    class Meta:
        model = Inquiry
        fields = '__all__'

class InquiryRetrieveSerializers(serializers.ModelSerializer):
    courses = CourseSerializers(read_only=True,many=True)
    colleges = CollegeSerializers(read_only=True,many=True)
    class Meta:
        model = Inquiry
        fields = '__all__'

class InquiryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'