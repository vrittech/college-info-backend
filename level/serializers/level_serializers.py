from rest_framework import serializers
from ..models import Level, SubLevel

class SubLevelSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        fields = '__all__'

class LevelListSerializers(serializers.ModelSerializer):
    sublevel = SubLevelSerializers(many=True, read_only=True)
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