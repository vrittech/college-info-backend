from rest_framework import serializers
from ..models import Discipline

class DisciplineListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

class DisciplineRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'

class DisciplineWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'