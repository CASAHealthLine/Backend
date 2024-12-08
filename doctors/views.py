from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Specialty
from .serializers import DoctorSerializer, SpecialtySerializer

class SpecialtyListView(APIView):
    def get(self, request):
        specialty = Specialty.objects.all()
        serializer = SpecialtySerializer(specialty, many=True)
        return Response(serializer.data)

class DoctorListView(APIView):
    def get(self, request):
        pass
    
class DoctorDetailView(APIView):
    def get(self, request, doctor_id):
        pass
    
class DoctorAddView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if not user.is_superuser:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        