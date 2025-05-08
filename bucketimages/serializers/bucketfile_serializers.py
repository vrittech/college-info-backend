from rest_framework import serializers
from ..models import BucketFile

class BucketFileListSerializers(serializers.ModelSerializer):
    class Meta:
        model = BucketFile
        fields = '__all__'

class BucketFileRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = BucketFile
        fields = '__all__'

class BucketFileWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = BucketFile
        fields = '__all__'