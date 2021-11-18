from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerPatient
from .serializers import DoctorSerializer
from .models import Doctor


class DoctorListCreateApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.filter(patient=self.request.patient)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.patient)


class DoctorRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerPatient)
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.filter(patient=self.request.patient)

    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        return super(DoctorRetrieveUpdateDestroyApiView, self).get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        return super(DoctorRetrieveUpdateDestroyApiView, self).put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        return super(DoctorRetrieveUpdateDestroyApiView, self).delete(request, *args, **kwargs)

