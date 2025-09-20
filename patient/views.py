from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Patient, HeartRate
from .serializers import PatientSerializer, HeartRateSerializer
from users.permissions import IsDoctor, IsHOD, IsPatient
from .filters import PatientFilter, HeartRateFilter

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Doctors and HODs to manage patients.
    Supports filtering by name and age.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor | IsHOD]
    filterset_class = PatientFilter
    
    def get_queryset(self):

                
        if getattr(self, 'swagger_fake_view', False):
            return Patient.objects.none()

        user = self.request.user
        if user.role == 'HOD':
            return Patient.objects.all()
        elif user.role == 'DOCTOR':
            return Patient.objects.filter(doctor=user)
        return Patient.objects.none()

class HeartRateListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating heart rate records for a specific patient.
    - Doctors can create/view heart rates for their patients.
    - Patients can only view their own heart rate history.
    - Supports filtering by date range.
    """
    serializer_class = HeartRateSerializer
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient]
    filterset_class = HeartRateFilter

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return HeartRate.objects.none()
        patient_pk = self.kwargs['patient_pk']
        user = self.request.user
        
        # Ensure the user has permission to view this patient's data
        if user.role == 'PATIENT':
            # A patient can only see their own data
            return HeartRate.objects.filter(patient__user=user, patient_id=patient_pk)
        elif user.role == 'DOCTOR':
            # A doctor can only see data for patients they manage
            return HeartRate.objects.filter(patient__doctor=user, patient_id=patient_pk)
        
        return HeartRate.objects.none()

    def perform_create(self, serializer):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
            
            # A doctor can only create heart rate data for their own patients
        if self.request.user != patient.doctor:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to add data for this patient.")

        serializer.save(patient=patient)

    