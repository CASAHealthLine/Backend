from django.contrib import admin

from patients.models import HealthRecord, Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'email', 'verified', 'created_at')
    search_fields = ('full_name', 'phone', 'email')
    
    list_filter = ('verified',)
    ordering = ('-created_at',)
    
@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'visit_date', 'created_at')
    search_fields = ('patient__full_name', 'doctor__full_name')
    
    list_filter = ('doctor', 'visit_date')
    ordering = ('-created_at',)