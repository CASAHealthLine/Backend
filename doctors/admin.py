from django.contrib import admin

from doctors.models import Doctor, Specialty

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'specialty', 'phone', 'email', 'employment_date')
    search_fields = ('full_name', 'phone', 'email')
    
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')