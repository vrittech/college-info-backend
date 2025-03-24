from django_filters import rest_framework as filters
from ..models import SubLevel  # Replace with your actual model

# Custom InFilter to support filtering with multiple values
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class SubLevelFilter(filters.FilterSet):
    # Supports both:
    # - /?level=1 (single value)
    # - /?level=1,2,3 (comma-separated)
    level = NumberInFilter(field_name='level', lookup_expr='in')
    
    # Other filters as before
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='exact')
    is_show = filters.BooleanFilter(field_name='is_show', lookup_expr='exact')
    created_date = filters.DateFilter(field_name='created_date', lookup_expr='exact')
    created_date__gte = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    created_date__lte = filters.DateFilter(field_name='created_date', lookup_expr='lte')

    class Meta:
        model = SubLevel
        fields = [
            'id', 'name', 'level', 'is_show',
            'created_date', 'created_date__gte', 'created_date__lte'
        ]