from django_filters import rest_framework as filters
from ..models import Inquiry


class InquiryFilter(filters.FilterSet):
    courses = filters.CharFilter(field_name='courses__slug', lookup_expr='icontains')  # Filter by course name
    colleges = filters.CharFilter(field_name='colleges__slug', lookup_expr='icontains')  # Filter by college name
     # Allow multiple course IDs
    courses_id = filters.BaseInFilter(field_name='courses__id', lookup_expr='in')  
    colleges_id = filters.BaseInFilter(field_name='colleges__id', lookup_expr='in')
    class Meta:
        model = Inquiry
        fields = ['courses', 'colleges','courses_id','colleges_id']
