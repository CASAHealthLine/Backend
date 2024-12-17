from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from queues.models import Queue
from queues.utils import add_to_queue
from .models import HealthRecord, Patient
from .serializers import HealthRecordSerializer, PatientSerializer
from django.utils.timezone import now

from .models import Patient
from .serializers import PatientSerializer

def get_or_create_patient(cccd, data):
    patient = Patient.objects.filter(cccd=cccd).first()
    data['verified'] = True
    
    if patient:
        serializer = PatientSerializer(patient, data=data, partial=True)
    else:
        serializer = PatientSerializer(data=data, partial=True)
    
    if serializer.is_valid():
        patient = serializer.save()
        return patient, not bool(patient.id)
    return None, serializer.errors

class UpdatePatientView(APIView):
    def post(self, request):
        cccd = request.data.get('cccd')
        
        if not cccd:
            return Response({"error": "Không tìm thấy CCCD"}, status=status.HTTP_400_BAD_REQUEST)
        
        patient, result = get_or_create_patient(cccd, request.data)
        
        if isinstance(result, dict):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "patient_id": patient.id
        }, status=status.HTTP_200_OK if patient else status.HTTP_201_CREATED)

class AddTreatmentView(APIView):
    def post(self, request):
        patient_data = request.data.get('patient')

        if not patient_data or not patient_data.get('cccd'):
            return Response({"error": "Missing cccd or treatment"}, status=status.HTTP_400_BAD_REQUEST)

        patient, result = get_or_create_patient(patient_data['cccd'], patient_data)
        
        if isinstance(result, dict):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        if Queue.objects.filter(patient=patient, date=now().date(), status=1 or 0).exists():
            return Response({"error": "Patient is already in the queue"}, status=status.HTTP_400_BAD_REQUEST)
        
        treatment_data = request.data.get('treatment')
        treatment_data['patient'] = patient.id
        treatment_data['visit_date'] = now().date()
        
        serializer = HealthRecordSerializer(data=treatment_data)
        if serializer.is_valid():
            health_record = serializer.save()
            add_to_queue(treatment_data['room_id'], patient.id, health_record.id)
            return Response({
                "health_record_id": health_record.id
            }, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetPatientByCCCD(APIView):
    def get(self, request, cccd):
        patient = Patient.objects.filter(cccd=cccd).first()
        if not patient:
            return Response({"error": "Không tìm thấy bệnh nhân"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)