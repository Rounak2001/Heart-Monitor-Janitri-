from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    """Custom User model for additional field """
    class Role(models.TextChoices):
        DOCTOR = "DOCTOR","doctor"
        PATIENT = "PATIENT","patient"
        HOD = "HOD","hod"
    role = models.CharField(max_length=50,choices=Role.choices)


    
       # Add this method
    def save(self, *args, **kwargs):
        # If the user is being made a superuser, automatically assign the HOD role.
        if self.is_superuser:
            self.role = self.Role.HOD
        super().save(*args, **kwargs) # Call the original save method
    
    def __str__(self):
        return f"{self.username} ({self.role})"
