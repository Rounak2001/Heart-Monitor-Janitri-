from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, DoctorCreationSerializer, PatientCreationSerializer
from .models import CustomUser
from patient.models import Patient
from .permissions import IsHOD, IsDoctor
from rest_framework.permissions import IsAuthenticated

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CreateDoctorView(generics.CreateAPIView):
    queryset =CustomUser.objects.all()
    serializer_class = DoctorCreationSerializer
    permission_classes = [IsHOD]

class CreatePatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreationSerializer
    # permission_classes = [IsDoctor]
    permission_classes = [IsAuthenticated, IsDoctor | IsHOD] 


    def get_serializer_context(self):
        """
        Pass the request object to the serializer.
        This is needed to get the logged-in doctor.
        """
        return {'request': self.request}