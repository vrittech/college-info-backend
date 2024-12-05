from rest_framework import serializers
from ..models import Duration

class DurationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = '__all__'

class DurationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = '__all__'

class DurationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = '__all__'