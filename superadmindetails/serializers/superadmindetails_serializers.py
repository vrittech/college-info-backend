from rest_framework import serializers
from ..models import SuperAdminDetails

class SuperAdminDetailsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminDetails
        fields = '__all__'

class SuperAdminDetailsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminDetails
        fields = '__all__'

class SuperAdminDetailsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdminDetails
        fields = '__all__'