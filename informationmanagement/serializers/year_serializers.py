from rest_framework import serializers
from ..models import Year

class YearListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class YearRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'

class YearWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'