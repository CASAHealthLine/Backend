from django.urls import path
from .views import get_notes , CustomTokenObtainPairView, CustomTokenRefreshView, logout, is_authenticated, register
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('notes/', get_notes),
    path('logout/', logout),
    path('authenticated/', is_authenticated),
    path('register/', register)
]