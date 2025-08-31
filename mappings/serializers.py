from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorListSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model.
    Includes nested patient and doctor information.
    """
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorListSerializer(source='doctor', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_details', 'doctor_details',
            'assigned_date', 'status', 'status_display', 'notes',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'assigned_date', 'created_by', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Custom validation for the mapping.
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        status = attrs.get('status', 'active')
        
        # Check if the patient belongs to the current user
        request = self.context.get('request')
        if request and patient.created_by != request.user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        
        # Check if the doctor is active
        if not doctor.is_active:
            raise serializers.ValidationError("Cannot assign an inactive doctor.")
        
        # Check for existing active mapping
        instance = getattr(self, 'instance', None)
        existing_mapping = PatientDoctorMapping.objects.filter(
            patient=patient, 
            doctor=doctor, 
            status=status
        )
        
        if instance:
            existing_mapping = existing_mapping.exclude(id=instance.id)
            
        if existing_mapping.exists() and status == 'active':
            raise serializers.ValidationError(
                f"Patient {patient.full_name} is already actively assigned to Dr. {doctor.full_name}"
            )
        
        return attrs


class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new patient-doctor mappings.
    """
    class Meta:
        model = PatientDoctorMapping
        fields = ['patient', 'doctor', 'status', 'notes']

    def validate(self, attrs):
        """
        Custom validation for the mapping creation.
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        status = attrs.get('status', 'active')
        
        # Check if the patient belongs to the current user
        request = self.context.get('request')
        if request and patient.created_by != request.user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        
        # Check if the doctor is active
        if not doctor.is_active:
            raise serializers.ValidationError("Cannot assign an inactive doctor.")
        
        # Check for existing active mapping
        if PatientDoctorMapping.objects.filter(
            patient=patient, 
            doctor=doctor, 
            status='active'
        ).exists() and status == 'active':
            raise serializers.ValidationError(
                f"Patient {patient.full_name} is already actively assigned to Dr. {doctor.full_name}"
            )
        
        return attrs


class PatientDoctorMappingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing mappings.
    """
    class Meta:
        model = PatientDoctorMapping
        fields = ['status', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional for updates
        for field in self.fields.values():
            field.required = False
