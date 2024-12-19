from django.urls import path
from .views import UpdatePatientView, AddTreatmentView, GetPatientByCCCD

urlpatterns = [
    path('update/', UpdatePatientView.as_view(), name='update_patient'),
    path('treatment/add/', AddTreatmentView.as_view(), name='add_treatment'),
    path('cccd/<str:cccd>/', GetPatientByCCCD.as_view(), name='get_patient_by_cccd'),
]