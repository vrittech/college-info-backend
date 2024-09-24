from rest_framework import serializers
from ..models import AdmissionOpen

class AdmissionOpenListSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdmissionOpen
        fields = '__all__'

class AdmissionOpenRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdmissionOpen
        fields = '__all__'

class AdmissionOpenWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdmissionOpen
        fields = '__all__'