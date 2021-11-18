from django.urls import path
from .views import PatientListCreateApiView, PatientDestroyUpdateApiView, GetPatientByCode

urlpatterns = [
    path('patients/', PatientListCreateApiView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDestroyUpdateApiView.as_view(), name='patient-delete-update'),
    path('get-patient/', GetPatientByCode.as_view(), name='patient-header')
]
