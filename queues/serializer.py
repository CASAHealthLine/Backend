from rest_framework import serializers
from .models import Queue

class QueueSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    patient_id = serializers.IntegerField(source='patient.id')
    patient_name = serializers.CharField(source='patient.full_name')
    room_id = serializers.IntegerField(source='room.id')
    room_name = serializers.CharField(source='room.displayname')
    cccd = serializers.CharField(source='patient.cccd')
    gender = serializers.CharField(source='patient.get_gender_display')
    birth_date = serializers.DateField(source='patient.birth_date')
    
    class Meta:
        model = Queue
        fields = '__all__'
        read_only_fields = ['status_display', 'patient_id', 'patient_name', 'room_id', 'room_name', 'cccd', 'gender', 'birth_date']
        
    def get_status_display(self, obj):
        return obj.get_status_display()