from .models import Patient
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Patient
        fields = ('id', 'name', 'code')
