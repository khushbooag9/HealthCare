from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient model.
    This allows managing patients from Django admin interface.
    """
    list_display = ['full_name', 'email', 'phone', 'gender', 'created_by', 'created_at']
    list_filter = ['gender', 'created_at', 'created_by']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Medical Information', {
            'fields': ('blood_group', 'allergies', 'medical_history')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
