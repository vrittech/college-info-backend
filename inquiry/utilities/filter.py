from django_filters import rest_framework as filters
from ..models import Inquiry

class InquiryFilter(filters.FilterSet):
    courses = filters.CharFilter(field_name='courses__name', lookup_expr='icontains')  # Filter by course name
    colleges = filters.CharFilter(field_name='colleges__name', lookup_expr='icontains')  # Filter by college name

    class Meta:
        model = Inquiry
        fields = ['courses', 'colleges']
