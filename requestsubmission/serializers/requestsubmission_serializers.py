from rest_framework import serializers
from ..models import RequestSubmission

class RequestSubmissionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequestSubmission
        fields = '__all__'

class RequestSubmissionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequestSubmission
        fields = '__all__'

class RequestSubmissionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequestSubmission
        fields = '__all__'