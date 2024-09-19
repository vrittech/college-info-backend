from rest_framework import serializers
from ..models import Affiliation

class AffiliationListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

class AffiliationRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'

class AffiliationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'