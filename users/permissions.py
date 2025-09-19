from rest_framework.permissions import BasePermission
from.models import CustomUser

class IsHOD(BasePermission):
    """
    Alows only Hod
    """
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == CustomUser.Role.HOD

class IsDoctor(BasePermission):
    """
    Allows Only Doctor
    """
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == CustomUser.Role.DOCTOR
    
class IsPatient(BasePermission):
    """
    Allows only Patient
    """
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == CustomUser.Role.PATIENT