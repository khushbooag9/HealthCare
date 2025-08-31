from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model.
    This handles serialization/deserialization of doctor data.
    """
    full_name = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'license_number', 'specialization', 'specialization_display',
            'experience_years', 'qualification', 'hospital_name', 'hospital_address',
            'city', 'state', 'consultation_fee', 'availability', 'bio',
            'created_by', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Check that the email is unique, except for the current instance.
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.email == value:
            return value
        
        if Doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_license_number(self, value):
        """
        Check that the license number is unique, except for the current instance.
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.license_number == value:
            return value
        
        if Doctor.objects.filter(license_number=value).exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return value


class DoctorCreateSerializer(DoctorSerializer):
    """
    Serializer for creating new doctors.
    """
    pass


class DoctorUpdateSerializer(DoctorSerializer):
    """
    Serializer for updating existing doctors.
    Makes all fields optional for partial updates.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional for updates
        for field in self.fields.values():
            field.required = False


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for doctor listing.
    Shows only essential information for better performance.
    """
    full_name = serializers.ReadOnlyField()
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'specialization', 'specialization_display',
            'hospital_name', 'city', 'consultation_fee', 'experience_years', 'is_active'
        ]
