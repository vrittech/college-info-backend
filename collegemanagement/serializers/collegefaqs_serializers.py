from rest_framework import serializers
from ..models import CollegeFaqs,College

class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id','slug','name']

class CollegeFaqsListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    class Meta:
        model = CollegeFaqs
        fields = '__all__'

class CollegeFaqsRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    class Meta:
        model = CollegeFaqs
        fields = '__all__'

class CollegeFaqsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeFaqs
        fields = '__all__'
    
    # def validate(self, attrs):
    #     # raise Exception("stopped")
    #     return super().validate(attrs)