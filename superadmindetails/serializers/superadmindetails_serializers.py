from rest_framework import serializers
from ..models import SuperAdminDetails

class SuperAdminDetailsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminDetails
        fields = ['name', 'email', 'phone_number', 'location', 'messenger_link', 'facebook_link', 'x_link', 'youtube_link', 'linkedin_link',]
        

class SuperAdminDetailsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminDetails
        fields = ['name', 'email', 'phone_number', 'location', 'messenger_link', 'facebook_link', 'x_link', 'youtube_link', 'linkedin_link',]

class SuperAdminDetailsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminDetails
        fields = '__all__'