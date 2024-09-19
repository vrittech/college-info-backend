from rest_framework import serializers
from ..models import InformationTagging

class InformationTaggingListSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationTagging
        fields = '__all__'

class InformationTaggingRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationTagging
        fields = '__all__'

class InformationTaggingWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationTagging
        fields = '__all__'