from rest_framework import serializers
from ..models import EmailSetup

class EmailSetupListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailSetup
        fields = '__all__'

class EmailSetupRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailSetup
        fields = '__all__'

class EmailSetupWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailSetup
        fields = '__all__'