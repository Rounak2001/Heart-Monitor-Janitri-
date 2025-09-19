# patients/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from .models import Patient

class PatientAPITests(APITestCase):
    def setUp(self):
        """
        Set up the initial data for all tests.
        """
        # Create CustomUsers with different roles
        self.hod = CustomUser.objects.create_user(username='hod', password='password123', role=CustomUser.Role.HOD)
        self.doctor1 = CustomUser.objects.create_user(username='doctor1', password='password123', role=CustomUser.Role.DOCTOR)
        self.doctor2 = CustomUser.objects.create_user(username='doctor2', password='password123', role=CustomUser.Role.DOCTOR)
        
        # Create a patient user and profile for doctor1
        self.patient1_user = CustomUser.objects.create_user(username='patient1', password='password123', role=CustomUser.Role.PATIENT)
        self.patient1 = Patient.objects.create(user=self.patient1_user, doctor=self.doctor1, full_name='Patient One', age=30)

        # Create a patient user and profile for doctor2
        self.patient2_user = CustomUser.objects.create_user(username='patient2', password='password123', role=CustomUser.Role.PATIENT)
        self.patient2 = Patient.objects.create(user=self.patient2_user, doctor=self.doctor2, full_name='Patient Two', age=40)

    ## Patient Management Tests
    
    def test_doctor_can_list_only_their_patients(self):
        """
        Ensure a doctor can only see the patients they manage. This is a critical data segregation test.
        """
        # Log in as doctor1
        self.client.force_authenticate(user=self.doctor1)
        
        url = reverse('patient-list') # Assumes 'patient-list' is the name from your router
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Doctor1 should only see 1 patient
        self.assertEqual(len(response.data['results']), 1)
        # Check that the patient seen is indeed patient1
        self.assertEqual(response.data['results'][0]['full_name'], self.patient1.full_name)

    def test_patient_cannot_list_patients(self):
        """
        Ensure a user with the patient role cannot access the patient list endpoint.
        """
        self.client.force_authenticate(user=self.patient1_user)
        
        url = reverse('patient-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hod_can_list_all_patients(self):
        """

        Ensure a user with the HOD role can see all patients from all doctors.
        """
        self.client.force_authenticate(user=self.hod)
        
        url = reverse('patient-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The HOD should see both patients
        self.assertEqual(len(response.data['results']), 2)

    ## Heart Rate Management Tests

    def test_doctor_can_create_heart_rate_for_own_patient(self):
        """
        Ensure a doctor can add a heart rate record for a patient they manage.
        """
        self.client.force_authenticate(user=self.doctor1)
        
        url = reverse('patient-heart-rates', kwargs={'patient_pk': self.patient1.pk})
        data = {'value': 85}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['value'], 85)

    def test_doctor_cannot_create_heart_rate_for_other_doctor_patient(self):
        """
        Ensure a doctor CANNOT add a heart rate record for another doctor's patient.
        """
        # Log in as doctor1
        self.client.force_authenticate(user=self.doctor1)
        
        # Try to add data for patient2 (who belongs to doctor2)
        url = reverse('patient-heart-rates', kwargs={'patient_pk': self.patient2.pk})
        data = {'value': 90}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_can_list_own_heart_rates(self):
        """
        Ensure a patient can view their own heart rate history.
        """
        # First, create a heart rate record for patient1
        self.test_doctor_can_create_heart_rate_for_own_patient()
        
        # Log in as patient1
        self.client.force_authenticate(user=self.patient1_user)
        
        url = reverse('patient-heart-rates', kwargs={'patient_pk': self.patient1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['value'], 85)

    def test_patient_cannot_list_other_patient_heart_rates(self):
        """
        Ensure a patient CANNOT view another patient's heart rate history.
        """
        self.client.force_authenticate(user=self.patient1_user)
        
        # Patient1 tries to access Patient2's data
        url = reverse('patient-heart-rates', kwargs={'patient_pk': self.patient2.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The queryset should be empty due to view's filtering logic
        self.assertEqual(len(response.data['results']), 0)