from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    Model to map patients to doctors.
    This represents the relationship between a patient and their assigned doctors.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    ]

    # Relationship fields
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    
    # Assignment details
    assigned_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the assignment")
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a patient can't be assigned to the same doctor multiple times with active status
        unique_together = ['patient', 'doctor', 'status']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.full_name} -> {self.doctor.full_name} ({self.status})"

    def clean(self):
        """
        Custom validation to ensure the patient belongs to the user creating the mapping.
        """
        from django.core.exceptions import ValidationError
        if self.patient.created_by != self.created_by:
            raise ValidationError("You can only assign doctors to your own patients.")
