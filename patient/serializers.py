from rest_framework import serializers
from .models import Patient, HeartRate

class HeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRate
        fields = ['id', 'patient', 'value', 'timestamp']
        read_only_fields = ['patient'] # Patient is set automatically from the URL

class PatientSerializer(serializers.ModelSerializer):
    # Use ReadOnlyField to show the username instead of just the user ID
    user_username = serializers.ReadOnlyField(source='user.username')
    doctor_username = serializers.ReadOnlyField(source='doctor.username')

    class Meta:
        model = Patient
        fields = [
            'id', 
            'full_name', 
            'age', 
            'address', 
            'contact_number', 
            'blood_group',
            'user',        # The patient's own user ID
            'user_username',
            'doctor',      # The doctor's user ID
            'doctor_username'
        ]