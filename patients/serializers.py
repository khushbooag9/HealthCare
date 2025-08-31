from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    This handles serialization/deserialization of patient data.
    """
    full_name = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'zip_code',
            'blood_group', 'allergies', 'medical_history', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Check that the email is unique, except for the current instance.
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.email == value:
            return value
        
        if Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value


class PatientCreateSerializer(PatientSerializer):
    """
    Serializer for creating new patients.
    Inherits from PatientSerializer but can add specific create validation.
    """
    pass


class PatientUpdateSerializer(PatientSerializer):
    """
    Serializer for updating existing patients.
    Makes all fields optional for partial updates.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional for updates
        for field in self.fields.values():
            field.required = False
