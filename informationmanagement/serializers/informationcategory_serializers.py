from rest_framework import serializers
from ..models import InformationCategory

class InformationCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = '__all__'

class InformationCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = '__all__'

class InformationCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = '__all__'