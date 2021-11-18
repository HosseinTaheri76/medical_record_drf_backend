from .models import Visit, Document
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VisitSerializer, DocumentSerializer
from .permissions import IsOwnerPatient
from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView


# Create your views here.

class VisitListCreateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_set = Visit.objects.filter(patient=request.patient)
        serializer = VisitSerializer(query_set, many=True, patient=request.patient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VisitSerializer(data=request.data, patient=request.patient, context={'request': request})
        if serializer.is_valid():
            serializer.save(patient=request.patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitRetrieveUpdateDeleteApiView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerPatient)

    def get_object(self, request, pk):
        return get_object_or_404(Visit, patient=request.patient, id=pk)

    def get(self, request, pk):
        qs = self.get_object(request, pk)
        self.check_object_permissions(request, qs)
        serializer = VisitSerializer(qs, patient=request.patient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        qs = self.get_object(request, pk)
        self.check_object_permissions(request, qs)
        serializer = VisitSerializer(instance=qs,
                                     data=request.data,
                                     patient=request.patient,
                                     partial=True,
                                     context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = self.get_object(request, pk)
        self.check_object_permissions(request, qs)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentListApiView(ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        doc_type = self.kwargs['doc_type']
        return Document.objects.filter(doc_type=doc_type, patient=self.request.patient)


class DocumentCreateApiView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(patient=self.request.patient)


class DocumentRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated, IsOwnerPatient)

    def get_queryset(self):
        doc_type = self.kwargs['doc_type']
        return Document.objects.filter(doc_type=doc_type, patient=self.request.patient)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(),
                                           data=request.data,
                                           context={'request': request},
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentSearchApiView(ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        doc_type = self.kwargs['doc_type']
        request = self.request
        if request.GET:
            if any(request.GET.values()):
                search_q = {arg: value for arg, value in request.GET.items()}
                search_q['doc_type'] = doc_type
                return Document.objects.search(**search_q).filter(patient=request.patient)
        return Document.objects.filter(doc_type__exact=doc_type, patient=request.patient)


class VisitSearchApiView(ListAPIView):
    serializer_class = VisitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        request = self.request
        if request.GET:
            search_q = {arg: value for arg, value in request.GET.items()}
            return Visit.objects.search(**search_q).filter(patient=request.patient)
        return Visit.objects.filter(patient=request.patient)

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(),
                                           patient=self.request.patient,
                                           many=True,
                                           context={'request': self.request})
        return Response(serializer.data, status= status.HTTP_200_OK)
