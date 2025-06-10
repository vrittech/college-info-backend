from rest_framework import serializers
from ..models import Result

class ResultListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id','symbol_no', 'dateofbirth', 'cgpa', 'remarks']

class ResultRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id','symbol_no', 'dateofbirth', 'cgpa', 'remarks']

class ResultWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'