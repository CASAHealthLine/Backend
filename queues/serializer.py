from rest_framework import serializers
from .models import Queue

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ['id', 'patient', 'room', 'status', 'created_at', 'updated_at']
