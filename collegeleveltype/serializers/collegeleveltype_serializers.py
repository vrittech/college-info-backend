from rest_framework import serializers
from ..models import CollegeLevelType

class CollegeLevelTypeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeLevelType
        fields = '__all__'

class CollegeLevelTypeRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeLevelType
        fields = '__all__'

class CollegeLevelTypeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeLevelType
        fields = '__all__'