import os
from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Lấy refresh token từ cookie
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not found in cookies'}, status=status.HTTP_401_UNAUTHORIZED)

        # Gắn refresh token vào request data để làm mới token
        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        # Trả access token mới
        if response.status_code == 200:
            return Response({
                'access': response.data.get('access')
            }, status=status.HTTP_200_OK)
        
        # Trường hợp làm mới thất bại
        return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

class ReactAppView(View):
    def get(self, request):
        try:
            with open('../Frontend/dist/index.html') as file:
                return HttpResponse(file.read())
        except FileNotFoundError:
            return HttpResponseNotFound("React build files not found.")