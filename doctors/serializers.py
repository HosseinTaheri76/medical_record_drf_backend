from .models import Doctor
from rest_framework import serializers


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'file_no', 'clinic_phone')
