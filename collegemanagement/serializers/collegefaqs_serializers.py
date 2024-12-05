from rest_framework import serializers
from ..models import CollegeFaqs

class CollegeFaqsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeFaqs
        fields = '__all__'

class CollegeFaqsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeFaqs
        fields = '__all__'

class CollegeFaqsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollegeFaqs
        fields = '__all__'