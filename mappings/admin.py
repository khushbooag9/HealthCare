from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """
    Admin configuration for PatientDoctorMapping model.
    """
    list_display = ['patient', 'doctor', 'status', 'assigned_date', 'created_by']
    list_filter = ['status', 'assigned_date', 'created_by']
    search_fields = [
        'patient__first_name', 'patient__last_name',
        'doctor__first_name', 'doctor__last_name'
    ]
    readonly_fields = ['assigned_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('patient', 'doctor', 'status', 'notes')
        }),
        ('System Information', {
            'fields': ('created_by', 'assigned_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Optimize queries by selecting related objects.
        """
        return super().get_queryset(request).select_related('patient', 'doctor', 'created_by')
