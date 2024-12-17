from rest_framework import serializers

from .models import HealthRecord, Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        
class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = '__all__'