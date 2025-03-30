from rest_framework import serializers
from ..models import InformationCategory

class InformationCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = [
            'id', 
            'name', 
            'slug', 
            'is_show', 
            'image',
            'information_count',  # Include the count
            'created_date',       # Optional
        ]
        # Optional: Make 'image' return full URL
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True}
        }
        def get_information_count(self, obj):
            return obj.information_set.count()

class InformationCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = [
            'id', 
            'name', 
            'slug', 
            'is_show', 
            'image',
            'information_count',  # Include the count
            'created_date',       # Optional
        ]
        # Optional: Make 'image' return full URL
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True}
        }
        def get_information_count(self, obj):
            return obj.information_set.count()

class InformationCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = '__all__'