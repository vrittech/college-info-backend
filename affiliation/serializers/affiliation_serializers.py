from rest_framework import serializers
from ..models import Affiliation
from district.models import District
import ast
from certification.models import Certification

def str_to_list(data, value_to_convert):
    try:
        mutable_data = data.dict()  # Convert to dictionary if possible
    except AttributeError:
        mutable_data = data  # Already a dictionary

    value_to_convert_data = mutable_data.get(value_to_convert)

    # If it's already a list, return as is
    if isinstance(value_to_convert_data, list):
        return mutable_data

    # Handle binary or file data (leave as is)
    if isinstance(value_to_convert_data, bytes):
        return mutable_data

    # If it's an int, float, or bool, wrap it in a list
    if isinstance(value_to_convert_data, (int, float, bool)):
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

    # If it's None, convert to an empty list
    if value_to_convert_data is None:
        mutable_data[value_to_convert] = []
        return mutable_data

    # Handle comma-separated values (e.g., "4,5")
    if isinstance(value_to_convert_data, str) and "," in value_to_convert_data:
        parsed_list = [item.strip() for item in value_to_convert_data.split(",")]
        # Convert to integers if possible
        mutable_data[value_to_convert] = [int(item) if item.isdigit() else item for item in parsed_list]
        return mutable_data

    # If it's a string, try parsing it as a list
    try:
        parsed_value = ast.literal_eval(value_to_convert_data)

        # Ensure parsed result is a list
        if isinstance(parsed_value, list):
            mutable_data[value_to_convert] = parsed_value
        else:
            # Convert string (that is not a list) into a single-item list
            mutable_data[value_to_convert] = [value_to_convert_data]

        return mutable_data

    except (ValueError, SyntaxError):
        # If parsing fails, wrap it in a list instead
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

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
        
class AffiliationListUserSerializers(serializers.ModelSerializer):
    district = DistrictSerializers(read_only=True)
    class Meta:
        model = Affiliation
        fields = ['id','slug','name','logo_image','cover_image','district','address']

class AffiliationRetrieveSerializers(serializers.ModelSerializer):
    district = DistrictSerializers(read_only=True)
    certification = CertificationSerializers(read_only=True,many = True)
    class Meta:
        model = Affiliation
        fields = '__all__'


class AffiliationWriteSerializers(serializers.ModelSerializer):
    # Accept ForeignKey and ManyToMany fields as IDs
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(),required=False,allow_null=True)
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