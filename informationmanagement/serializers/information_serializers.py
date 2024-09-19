from rest_framework import serializers
from ..models import Information

class InformationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class InformationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class InformationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'