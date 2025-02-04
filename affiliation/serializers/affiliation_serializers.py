from rest_framework import serializers
from ..models import Affiliation
from district.models import District
from certification.models import Certification

class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        ref_name='Affiliation'
        fields = '__all__'
        
class CertificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        ref_name='Affiliation'
        
        
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
    # Accept `certification` as a comma-separated string for input
    certification = serializers.CharField(write_only=True, required=False)

    # Include `certification` as a read-only field for the response
    certifications = serializers.SerializerMethodField()

    class Meta:
        model = Affiliation
        fields = '__all__'

    def validate_certification(self, value):
        """
        Converts a comma-separated string into a list of integers.
        """
        if value:
            try:
                # Split the string and convert to integers
                certification_ids = [int(pk.strip()) for pk in value.split(",") if pk.strip()]
                return certification_ids
            except ValueError:
                raise serializers.ValidationError("Certification must be a comma-separated list of valid integers.")
        return []

    def create(self, validated_data):
        # Extract certifications from the validated data
        certifications = validated_data.pop('certification', [])
        
        # Create the Affiliation instance
        affiliation = Affiliation.objects.create(**validated_data)

        # Associate certifications if provided
        if certifications:
            affiliation.certification.set(certifications)

        return affiliation

    def update(self, instance, validated_data):
        # Extract certifications from the validated data
        certifications = validated_data.pop('certification', None)

        # Update the instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update certifications if provided
        if certifications is not None:
            instance.certification.set(certifications)

        return instance

    def get_certifications(self, obj):
        """
        Get the certifications for the response.
        """
        return [cert.id for cert in obj.certification.all()]
