from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Doctor model.
    """
    list_display = ['full_name', 'specialization', 'hospital_name', 'city', 'consultation_fee', 'is_active', 'created_by']
    list_filter = ['specialization', 'city', 'is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'license_number', 'hospital_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('license_number', 'specialization', 'experience_years', 'qualification')
        }),
        ('Hospital Information', {
            'fields': ('hospital_name', 'hospital_address', 'city', 'state')
        }),
        ('Consultation Details', {
            'fields': ('consultation_fee', 'availability', 'bio')
        }),
        ('System Information', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
