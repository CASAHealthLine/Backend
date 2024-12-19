from django.urls import path
from .views import DoctorListView, SpecialtyListView, DoctorDetailView, DoctorAddView

urlpatterns = [
    path('specialty/', SpecialtyListView.as_view(), name='specialty_list'),
    path('doctor/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/<int:doctor_id>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctor/create/', DoctorAddView.as_view(), name='doctor_create'),
]