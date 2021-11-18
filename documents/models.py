from doctors.models import Doctor
from patients.models import Patient
from .uploaders import *
from datetime import date
from django.db import models
from django.db.models import Min, Max, Q


class VisitManager(models.Manager):
    def get_future_visits(self):
        today = date.today()
        return self.get_queryset().filter(visit_date__gt=today)

    def search(self, doctor_name=None, reason=None, visit_date_from=None, visit_date_to=None, future=None):
        base_qs = self.get_future_visits() if future else self.get_queryset()
        if visit_date_from:
            visit_date_start = visit_date_from
        else:
            visit_date_start = self.aggregate(min_date=Min('visit_date'))['min_date']
        if visit_date_to:
            visit_date_end = visit_date_to
        else:
            visit_date_end = self.aggregate(max_date=Max('visit_date'))['max_date']
        lookup = Q(visit_date__gte=visit_date_start) & Q(visit_date__lte=visit_date_end)
        if doctor_name:
            lookup &= Q(doctor_name__contains=doctor_name)
        if reason:
            lookup &= Q(reason__contains=reason)
        return base_qs.filter(lookup)


class DocumentManager(models.Manager):
    def search(self, doc_type, title=None, doc_date_from=None, doc_date_to=None):
        base_qs = self.get_queryset().filter(doc_type__exact=doc_type)
        if doc_date_from:
            doc_date_start = doc_date_from
        else:
            doc_date_start = self.aggregate(min_date=Min('doc_date'))['min_date']
        if doc_date_to:
            doc_date_end = doc_date_to
        else:
            doc_date_end = self.aggregate(max_date=Max('doc_date'))['max_date']
        lookup = Q(doc_date__gte=doc_date_start) & Q(doc_date__lte=doc_date_end)
        if title:
            lookup &= Q(title__icontains=title)
        return base_qs.filter(lookup)


# Create your models here.
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name='visits')
    doctor_name = models.CharField(max_length=150, null=True)
    reason = models.TextField(max_length=200)
    visit_date = models.DateField()
    next_visit = models.DateField(null=True, blank=True)
    file = models.ImageField(
        upload_to=prescription_img_uploader,
        null=True,
        blank=True
    )
    objects = VisitManager()

    def __str__(self):
        return f'{self.doctor.name}, {self.patient.name}, {self.visit_date}'


class Document(models.Model):
    DOC_TYPE_CHOICES = (
        ('sonography', 'sonography'),
        ('test', 'test'),
        ('image-scan', 'image-scan'),
        ('other', 'other')
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='docs')
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES)
    doc_date = models.DateField()
    title = models.CharField(max_length=100)
    file = models.FileField(
        upload_to=document_img_uploader,
        null=True,
        blank=True
    )
    objects = DocumentManager()

    def __str__(self):
        return f'{self.doc_type} {self.title}'
