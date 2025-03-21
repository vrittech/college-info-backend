import django_filters
from django_filters import rest_framework as filters
from ..models import Group 

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class GroupFilter(django_filters.FilterSet):
    id = NumberInFilter(field_name='id', lookup_expr='in')  # Filters for multiple IDs
    name = CharInFilter(field_name='name', lookup_expr='exact')  # Exact match for name
    class Meta:
        model = Group  # Replace with your actual model
        fields = ['id', 'name',]  # List the fields you want to filter by
