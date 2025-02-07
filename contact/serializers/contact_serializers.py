from rest_framework import serializers
from ..models import Contact
from accounts.models import CustomUser

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','full_name']

class ContactListSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Contact
        fields = '__all__'

class ContactRetrieveSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Contact
        fields = '__all__'

class ContactWriteSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Contact
        fields = '__all__'