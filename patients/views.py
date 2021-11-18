from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveAPIView
from .serializers import PatientSerializer
from .models import Patient
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from .permissions import IsPatientOwner


class PatientListCreateApiView(ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PatientDestroyUpdateApiView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated, IsPatientOwner)

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def put(self, request, pk):
        self.check_object_permissions(request, self.get_object())
        return self.update(request, pk)

    def delete(self, request, pk):
        self.check_object_permissions(request, self.get_object())
        return self.destroy(request, pk)


class GetPatientByCode(RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated, IsPatientOwner)

    def get_object(self):
        return self.request.patient

    def get(self, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return super().get(self.request, *args, **kwargs)
