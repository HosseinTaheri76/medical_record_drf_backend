from .models import Visit, Document
from rest_framework import serializers


class VisitSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient')
        super(VisitSerializer, self).__init__(*args, **kwargs)

    doctor_name = serializers.CharField(max_length=150, read_only=True, required=False)

    class Meta:
        model = Visit
        fields = ('id', 'doctor', 'doctor_name', 'reason', 'visit_date', 'next_visit', 'file')

    def validate_doctor(self, value):
        if value.id not in [doctor.id for doctor in self.patient.doctors.all()]:
            raise serializers.ValidationError('invalid Doctor')
        return value


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'doc_type', 'doc_date', 'file')

