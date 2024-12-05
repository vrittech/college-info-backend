from rest_framework import serializers
from ..models import SubLevel

class SubLevelListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        fields = '__all__'

class SubLevelRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        fields = '__all__'

class SubLevelWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        fields = '__all__'