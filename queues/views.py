from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.utils.timezone import now

from queues.filters import QueueFilter
from rooms.models import Room
from .models import Queue

class CustomPagination(PageNumberPagination):
    page_size = 10  # Số lượng bản ghi mặc định mỗi trang
    page_size_query_param = 'limit'  # Cho phép client tùy chỉnh giới hạn
    max_page_size = 100  # Giới hạn tối đa cho mỗi trang
