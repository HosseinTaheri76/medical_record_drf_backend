from django.urls import path
from .views import DoctorListCreateApiView, DoctorRetrieveUpdateDestroyApiView

urlpatterns = [
    path('doctors/', DoctorListCreateApiView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateDestroyApiView.as_view(), name='doctor-R-U-D'),
]
