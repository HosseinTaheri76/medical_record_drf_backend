from django.db import models
from patients.models import Patient


# Create your models here.

class Doctor(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=150)
    file_no = models.IntegerField(null=True, blank=True)
    clinic_phone = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


