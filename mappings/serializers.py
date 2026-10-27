from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all()
    )
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all()
    )

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "assigned_at"]
        read_only_fields = ["id", "assigned_at"]

    def validate_patient(self, patient):
        request = self.context["request"]

        if patient.created_by != request.user:
            raise serializers.ValidationError(
                "You can only assign doctors to your own patients."
            )

        return patient