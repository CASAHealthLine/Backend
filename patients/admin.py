from django.contrib import admin

from patients.models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'email', 'verified', 'created_at')
    search_fields = ('full_name', 'phone', 'email')