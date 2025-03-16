from django_filters import rest_framework as filters
from ..models import Inquiry


class InquiryFilter(filters.FilterSet):
    courses = filters.CharFilter(field_name='courses__slug', lookup_expr='icontains')  # Filter by course name
    colleges = filters.CharFilter(field_name='colleges__slug', lookup_expr='icontains')  # Filter by college name
     # Allow multiple course IDs
    courses_id = filters.BaseInFilter(field_name='courses__id', lookup_expr='in')  
    colleges_id = filters.BaseInFilter(field_name='colleges__id', lookup_expr='in')
    
    created_date = filters.DateFilter(field_name="created_date", lookup_expr="exact")
    created_date__gte = filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = filters.DateFilter(field_name="created_date", lookup_expr="lte")
    
    updated_date = filters.DateFilter(field_name="updated_date", lookup_expr="exact")
    updated_date__gte = filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = filters.DateFilter(field_name="updated_date", lookup_expr="lte")
    
    class Meta:
        model = Inquiry
        fields = ['courses', 'colleges','courses_id','colleges_id',"created_date","created_date__gte","created_date__lte","updated_date","updated_date__gte","updated_date__lte"]
