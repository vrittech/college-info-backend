from rest_framework import serializers
from ..models import Album

class AlbumListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'