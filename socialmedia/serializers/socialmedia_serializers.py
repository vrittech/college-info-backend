from rest_framework import serializers
from ..models import SocialMedia

class SocialMediaListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class SocialMediaRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class SocialMediaWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'