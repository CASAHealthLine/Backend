from django.urls import path
from .views import RegisterView, LoginView, AccountView, LogoutView, ResetPasswordView,RequestResetPasswordView, UserRoleView

urlpatterns = [
    path('user-role/', UserRoleView.as_view(), name='user-role'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-reset-password/', RequestResetPasswordView.as_view(), name='request-reset-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]