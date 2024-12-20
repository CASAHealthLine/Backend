from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from patients.models import HealthRecord, Patient
from queues.models import Queue
from rooms.models import Room
from django.utils.timezone import now

def add_to_queue(room_id, patient_id, health_record_id):
    room = get_object_or_404(Room, pk=room_id)
    patient = get_object_or_404(Patient, pk=patient_id)
    health_record = get_object_or_404(HealthRecord, pk=health_record_id)
    
    # Check if the patient is already in the queue
    if Queue.objects.filter(patient=patient, room=room, created_at__date=now().date()).exists():
        return Response({"error": "Patient is already in the queue"}, status=status.HTTP_400_BAD_REQUEST)
    
    queue = Queue.objects.create(patient=patient, room=room, health_record=health_record)
    return Response({
        "queue_id": queue.id
    }, status=status.HTTP_201_CREATED)