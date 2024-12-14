from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from rooms.models import Room
from .models import Queue

class CustomPagination(PageNumberPagination):
    page_size = 10  # Số lượng bản ghi mặc định mỗi trang
    page_size_query_param = 'limit'  # Cho phép client tùy chỉnh giới hạn
    max_page_size = 100  # Giới hạn tối đa cho mỗi trang

class AddToQueueView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.type == 0:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        patient_id = request.data.get('patient_id')
        room_id = request.data.get('room_id')

        if not patient_id or not room_id:
            return Response({"error": "Missing patient_id or room_id"}, status=status.HTTP_400_BAD_REQUEST)

        existing_queue = Queue.objects.filter(patient_id=patient_id, room_id=room_id, status='waiting').first()
        if existing_queue:
            return Response(
                {"message": "Patient already in queue", "queue_id": existing_queue.id},
                status=status.HTTP_200_OK
            )

        queue = Queue.objects.create(patient_id=patient_id, room_id=room_id)
        return Response({"message": "Patient added to queue", "queue_id": queue.id}, status=status.HTTP_201_CREATED)
    
class GetSpecificQueueView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, room_id):
        queues = Queue.objects.filter(room_id=room_id, status='waiting').order_by('created_at')
        data = [
            {
                "queue_id": queue.id,
                "patient_id": queue.patient.id,
                "patient_name": queue.patient.full_name,
                "status": queue.status,
                "created_at": queue.created_at
            } for queue in queues
        ]
        return Response(data, status=status.HTTP_200_OK)
    
class UpdateQueueStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, queue_id):
        status = request.data.get('status')
        if not status:
            return Response({"error": "Missing status"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queue = Queue.objects.get(id=queue_id)
            queue.status = status
            queue.save()
            return Response({"message": "Queue status updated"}, status=status.HTTP_200_OK)
        except Queue.DoesNotExist:
            return Response({"error": "Queue not found"}, status=status.HTTP_404_NOT_FOUND)

class GetQueueView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        client_ip = request.headers.get('X-Client-IP', None)
        
        # Tìm phòng dựa trên IP
        room = Room.objects.filter(ip_address=client_ip).first()
        base_queryset = Queue.objects.all().order_by('status', 'created_at')
        
        if not room or user.type == 0:
            queues = base_queryset.filter(patient_id=user.id)
        elif user.type == 1:
            if room and room.type.type_name == 'reception':
                queues = base_queryset
            elif room:
                queues = base_queryset.filter(room_id=room.id)
            else:
                queues = Queue.objects.none()
        else:
            queues = base_queryset
            
        queues = queues.select_related('patient', 'room').only(
            'id', 'patient__id', 'patient__full_name', 'room__id', 'room__displayname', 'status', 'created_at'
        )
        
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(queues, request)
        
        data = [
            {
                "queue_id": queue.id,
                "patient_id": queue.patient.id,
                "patient_name": queue.patient.full_name,
                "room_id": queue.room.id,
                "room_name": queue.room.displayname,
                "status": queue.status,
                "created_at": queue.created_at
            } for queue in result_page
        ]
        return paginator.get_paginated_response(data)