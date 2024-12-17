from django.urls import path

from rooms.views import get_rooms

urlpatterns = [
    path('list/', get_rooms, name='room_list'),
]