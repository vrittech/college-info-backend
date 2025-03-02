from rest_framework import serializers
from ..models import CollegeSocialMedia
from socialmedia.models import SocialMedia
from collegemanagement.models import College

class SocialMediaSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id','name','link']
        
class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        ref_name = 'CollegeSocialMediaSerializers'
        fields = ['id','name','slug']


class CollegeSocialMediaListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    name = SocialMediaSerializers(read_only=True)
    class Meta:
        model = CollegeSocialMedia
        fields = '__all__'

class CollegeSocialMediaRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    name = SocialMediaSerializers(read_only=True)
    class Meta:
        model = CollegeSocialMedia
        fields = '__all__'

class CollegeSocialMediaWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeSocialMedia
        fields = '__all__'
        