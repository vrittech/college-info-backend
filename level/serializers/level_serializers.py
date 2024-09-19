from rest_framework import serializers
from ..models import Level

class LevelListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class LevelRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class LevelWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'