from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Patient(models.Model):
    """ Patient Model"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name = "patient_profile"
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="patient_managed"
    )
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    address = models.TextField()
    contact_number = models.CharField(max_length=12,null=True,blank=True)
    blood_group = models.CharField(max_length=3)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.full_name
    
class HeartRate(models.Model):
    """Model To HeartRate Reading"""
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="heart_rates"
    )
    value = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.patient.full_name}-{self.value}"


