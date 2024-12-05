from rest_framework import serializers
from ..models import InformationFiles

class InformationFilesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationFiles
        fields = '__all__'

class InformationFilesRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationFiles
        fields = '__all__'

class InformationFilesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationFiles
        fields = '__all__'