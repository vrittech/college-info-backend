from rest_framework import serializers
from ..models import RequestSubmission
from accounts.models import CustomUser

class CustomUserRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name','college__name']

class RequestSubmissionListSerializers(serializers.ModelSerializer):
    user = CustomUserRequestSerializers(read_only=True)
    class Meta:
        model = RequestSubmission
        fields = '__all__'

class RequestSubmissionRetrieveSerializers(serializers.ModelSerializer):
    user = CustomUserRequestSerializers(read_only=True)
    class Meta:
        model = RequestSubmission
        fields = '__all__'

class RequestSubmissionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequestSubmission
        exclude = ['user']  # Exclude user from writable fields

    def create(self, validated_data):
        # user will be passed via context from the viewset
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Don't allow user to be updated manually
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
