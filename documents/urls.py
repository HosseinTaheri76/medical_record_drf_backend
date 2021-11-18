from django.urls import path
from .views import VisitListCreateApiView, VisitRetrieveUpdateDeleteApiView, DocumentListApiView, DocumentCreateApiView, \
    DocumentRetrieveUpdateDestroyApiView, VisitSearchApiView, DocumentSearchApiView

urlpatterns = [
    path('visits/', VisitListCreateApiView.as_view(), name='visit-list-create'),
    path('visits/<int:pk>/', VisitRetrieveUpdateDeleteApiView.as_view(), name='visit-R-U-D'),
    path('documents/<str:doc_type>/', DocumentListApiView.as_view(), name='doc-list'),
    path('create-document/', DocumentCreateApiView.as_view(), name='create-doc'),
    path('documents/<str:doc_type>/<int:pk>/', DocumentRetrieveUpdateDestroyApiView.as_view(), name='document-R-U-D'),
    path('visits/search/', VisitSearchApiView.as_view(), name='visit-search'),
    path('documents/search/<str:doc_type>/', DocumentSearchApiView.as_view(), name='document-search'),
]
