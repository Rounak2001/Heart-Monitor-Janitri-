from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, HeartRateListCreateView

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')

urlpatterns = [
    path('', include(router.urls)),
    path('patients/<int:patient_pk>/heart-rates/', HeartRateListCreateView.as_view(), name='patient-heart-rates'),
]