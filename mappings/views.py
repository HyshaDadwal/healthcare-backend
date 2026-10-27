from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related("patient", "doctor")

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = serializer.validated_data["patient"]
        doctor = serializer.validated_data["doctor"]

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor,
        ).exists():
            raise ValidationError(
                {"detail": "This doctor is already assigned to this patient."}
            )

        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class MappingDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        # GET /api/mappings/<patient_id>/
        patient = get_object_or_404(
            Patient,
            pk=pk,
            created_by=request.user,
        )

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related("patient", "doctor")

        serializer = PatientDoctorMappingSerializer(
            mappings,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        # DELETE /api/mappings/<mapping_id>/
        mapping = get_object_or_404(
            PatientDoctorMapping.objects.select_related("patient"),
            pk=pk,
            patient__created_by=request.user,
        )

        mapping.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)