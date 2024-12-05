from rest_framework import serializers
from ..models import FormStepProgress

class FormStepProgressListSerializers(serializers.ModelSerializer):
    class Meta:
        model = FormStepProgress
        fields = '__all__'

class FormStepProgressRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = FormStepProgress
        fields = '__all__'

class FormStepProgressWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = FormStepProgress
        fields = '__all__'