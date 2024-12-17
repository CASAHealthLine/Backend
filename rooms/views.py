from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rooms.models import Room

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.values('id', 'displayname', 'description')
    return Response(rooms)