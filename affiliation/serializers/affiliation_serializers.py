from rest_framework import serializers
from ..models import Affiliation
from district.models import District
import ast
from certification.models import Certification

def str_to_list(data,value_to_convert):
    try:
        mutable_data = data.dict()
    except Exception:
        mutable_data = data
    value_to_convert_data = mutable_data[value_to_convert]
    if isinstance(value_to_convert_data,list):# type(value_to_convert_data) == list:

        return mutable_data
    try:
        variations = ast.literal_eval(value_to_convert_data)
        mutable_data[value_to_convert] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({f'{value_to_convert}': str(e)}) from e

class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        ref_name='Affiliation_district'
        fields = ['id', 'name']
        
class CertificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'name']
        ref_name='Affiliation_certification'
        
        
class AffiliationListSerializers(serializers.ModelSerializer):
    district = DistrictSerializers(read_only=True)
    certification = CertificationSerializers(read_only=True,many = True)
    class Meta:
        model = Affiliation
        fields = '__all__'

class AffiliationRetrieveSerializers(serializers.ModelSerializer):
    district = DistrictSerializers(read_only=True)
    certification = CertificationSerializers(read_only=True,many = True)
    class Meta:
        model = Affiliation
        fields = '__all__'


class AffiliationWriteSerializers(serializers.ModelSerializer):
    # Accept ForeignKey and ManyToMany fields as IDs
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    certification = serializers.PrimaryKeyRelatedField(queryset=Certification.objects.all(), many=True)

    class Meta:
        model = Affiliation
        fields = '__all__'  # Dynamically include all fields in the model

    def to_internal_value(self, data):
        """Convert certification input from string to list using str_to_list."""
        data = str_to_list(data, 'certification')  # Convert string to list for certification
        return super().to_internal_value(data)

    def create(self, validated_data):
        """Handles creation of an affiliation."""
        certifications = validated_data.pop('certification', [])
        affiliation = Affiliation.objects.create(**validated_data)
        affiliation.certification.set(certifications)
        return affiliation

    def update(self, instance, validated_data):
        """Handles updates for an affiliation."""
        certifications = validated_data.pop('certification', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update many-to-many relationships if provided
        if certifications is not None:
            instance.certification.set(certifications)

        return instance
    
    def to_representation(self, instance):
        """Ensure the response includes all fields sent in the payload."""
        response = super().to_representation(instance)

        # Replace ForeignKey and ManyToMany fields with nested object representations
        response['district'] = DistrictSerializers(instance.district).data
        response['certification'] = CertificationSerializers(instance.certification.all(), many=True).data

        return response