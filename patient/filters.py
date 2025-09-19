import django_filters
from .models import Patient, HeartRate

class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        fields = {
            'full_name': ['icontains'], # Case-insensitive partial search on name
            'age': ['exact', 'gte', 'lte'], # Filter by exact age, greater than, or less than
        }

class HeartRateFilter(django_filters.FilterSet):
    # Allows filtering heart rates within a date range
    start_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = HeartRate
        fields = ['start_date', 'end_date', 'value']