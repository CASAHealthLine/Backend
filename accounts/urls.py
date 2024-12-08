from django.urls import path
from .views import RegisterView, LoginView, ProtectedView, LogoutView, ResetPasswordView,RequestResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-reset-password/', RequestResetPasswordView.as_view(), name='request-reset-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]