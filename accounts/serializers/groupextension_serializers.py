from rest_framework import serializers
from ..models import GroupExtension

class GroupExtensionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = GroupExtension
        fields = '__all__'

class GroupExtensionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = GroupExtension
        fields = '__all__'

class GroupExtensionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = GroupExtension
        fields = '__all__'