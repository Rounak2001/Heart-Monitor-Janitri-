from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from patient.models import Patient

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token['username'] = user.username
        token['role'] = user.role
        return token

class DoctorCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=CustomUser.Role.DOCTOR
        )
        return user

class PatientCreationSerializer(serializers.Serializer):
    # User fields
    username = serializers.CharField(max_length=150, write_only=True) 
    password = serializers.CharField(write_only=True)
    
    # Patient profile fields
    full_name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()
    address = serializers.CharField()
    contact_number = serializers.CharField(max_length=12, required=False, allow_blank=True)
    blood_group = serializers.CharField(max_length=3)

    def create(self, validated_data):
        with transaction.atomic():
           
            patient_user = CustomUser.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                role=CustomUser.Role.PATIENT
            )
            
            doctor = self.context['request'].user
            
            patient_profile = Patient.objects.create(
                user=patient_user,
                doctor=doctor,
                full_name=validated_data['full_name'],
                age=validated_data['age'],
                
                address=validated_data['address'],
                contact_number=validated_data.get('contact_number'),
                blood_group=validated_data['blood_group']
            )
        
        return patient_profile