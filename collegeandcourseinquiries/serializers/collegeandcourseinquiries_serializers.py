from rest_framework import serializers
from ..models import CollegeAndCourseInquiries

class CollegeAndCourseInquiriesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeAndCourseInquiries
        fields = '__all__'

class CollegeAndCourseInquiriesRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeAndCourseInquiries
        fields = '__all__'

class CollegeAndCourseInquiriesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeAndCourseInquiries
        fields = '__all__'