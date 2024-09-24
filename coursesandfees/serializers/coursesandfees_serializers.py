from rest_framework import serializers
from ..models import CoursesAndFees

class CoursesAndFeesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoursesAndFees
        fields = '__all__'

class CoursesAndFeesRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoursesAndFees
        fields = '__all__'

class CoursesAndFeesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoursesAndFees
        fields = '__all__'