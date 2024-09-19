from rest_framework import serializers
from ..models import Certification

class CertificationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class CertificationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class CertificationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'