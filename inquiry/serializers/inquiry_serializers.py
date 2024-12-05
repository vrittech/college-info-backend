from rest_framework import serializers
from ..models import Inquiry

class InquiryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

class InquiryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

class InquiryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'