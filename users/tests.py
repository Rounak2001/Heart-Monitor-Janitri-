
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser
from patient.models import Patient

class CustomUserAPITests(APITestCase):
    def setUp(self):
        """
        Set up initial users for testing the user creation endpoints.
        """
        self.hod_user = CustomUser.objects.create_user(username='test_hod', password='password123', role=CustomUser.Role.HOD)
        self.doctor_user = CustomUser.objects.create_user(username='test_doctor', password='password123', role=CustomUser.Role.DOCTOR)
        self.patient_user = CustomUser.objects.create_user(username='test_patient', password='password123', role=CustomUser.Role.PATIENT)



    def test_hod_can_create_doctor(self):
        """
        Ensure a user with the HOD role can successfully create a new doctor.
        """
        self.client.force_authenticate(user=self.hod_user)
        url = reverse('create_doctor')
        data = {
            "username": "newdoctor",
            "email": "newdoc@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="newdoctor", role=CustomUser.Role.DOCTOR).exists())

    def test_doctor_cannot_create_doctor(self):
        """
        Ensure a user with the Doctor role is forbidden from creating another doctor.
        """
        self.client.force_authenticate(user=self.doctor_user)
        url = reverse('create_doctor')
        data = {
            "username": "anotherdoctor",
            "email": "anotherdoc@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    


    def test_doctor_can_create_patient(self):
        """
        Ensure a doctor can create a new patient, which creates both a CustomUser and a Patient profile.
        """
        self.client.force_authenticate(user=self.doctor_user)
        url = reverse('create_patient')
        data = {
            "username": "newpatient",
            "password": "newpassword123",
            "full_name": "New Patient Name",
            "age": 50,
            "address": "123 Test Lane",
            "blood_group": "A+"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that both the CustomUser and Patient profile were created
        self.assertTrue(CustomUser.objects.filter(username="newpatient", role=CustomUser.Role.PATIENT).exists())
        self.assertTrue(Patient.objects.filter(full_name="New Patient Name").exists())
    
    def test_hod_cannot_create_patient_via_endpoint(self):
        """
        Ensure an HOD is forbidden from using the specific 'create-patient' endpoint.
        """
        self.client.force_authenticate(user=self.hod_user)
        url = reverse('create_patient')
        data = {
            "username": "anotherpatient",
            "password": "newpassword123",
            "full_name": "Another Patient",
            "age": 60,
            "address": "456 Test Ave",
            "blood_group": "B-"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

 
    
    def test_user_can_login_with_valid_credentials(self):
        """
        Ensure a user can successfully obtain an access and refresh token.
        """
        url = reverse('token_obtain_pair')
        data = {"username": "test_doctor", "password": "password123"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_cannot_login_with_invalid_credentials(self):
        """
        Ensure a user receives an unauthorized error with incorrect login details.
        """
        url = reverse('token_obtain_pair')
        data = {"username": "test_doctor", "password": "wrongpassword"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)