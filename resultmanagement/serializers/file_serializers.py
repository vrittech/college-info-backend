from rest_framework import serializers
from ..models import File

class FileListSerializers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FileRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FileWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'