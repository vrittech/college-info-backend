from rest_framework import serializers
from ..models import Contact

class ContactListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'