from rest_framework import serializers
from ..models import SubLevel, Level

class LevelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
        ref_name = 'LevelSerializers'

class SubLevelListSerializers(serializers.ModelSerializer):
    level = LevelSerializers(read_only=True)
    class Meta:
        model = SubLevel
        fields = '__all__'

class SubLevelRetrieveSerializers(serializers.ModelSerializer):
    level = LevelSerializers(read_only=True)
    class Meta:
        model = SubLevel
        fields = '__all__'

class SubLevelWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubLevel
        fields = '__all__'