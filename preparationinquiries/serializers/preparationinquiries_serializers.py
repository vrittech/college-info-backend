from rest_framework import serializers
from ..models import PreparationInquiries

class PreparationInquiriesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PreparationInquiries
        fields = '__all__'

class PreparationInquiriesRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = PreparationInquiries
        fields = '__all__'

class PreparationInquiriesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PreparationInquiries
        fields = '__all__'