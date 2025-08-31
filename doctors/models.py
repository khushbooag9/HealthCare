from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """
    Doctor model to store doctor information.
    Doctors can be assigned to patients.
    """
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('general_medicine', 'General Medicine'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('urology', 'Urology'),
        ('other', 'Other'),
    ]

    # Doctor basic information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    
    # Professional information
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    experience_years = models.PositiveIntegerField()
    qualification = models.CharField(max_length=200)
    
    # Hospital/Clinic information
    hospital_name = models.CharField(max_length=100)
    hospital_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    # Additional information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.TextField(help_text="Working hours and days")
    bio = models.TextField(blank=True, null=True)
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialization}"

    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"
