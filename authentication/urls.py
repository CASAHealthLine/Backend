from django.urls import path
from .views import LinkPhoneView, VerifyOTPView, RequestOTPView

urlpatterns = [
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('link-phone/', LinkPhoneView.as_view(), name='link-phone'),
    path('request-otp/', RequestOTPView.as_view(), name='request-otp'),
]