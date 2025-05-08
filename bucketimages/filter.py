# filter.py
import django_filters
from .models import BucketFile
from datetime import datetime

class BucketFileFilter(django_filters.FilterSet):
    min_size = django_filters.NumberFilter(field_name='size', lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name='size', lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name='last_modified', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='last_modified', lookup_expr='lte')
    extension = django_filters.CharFilter(field_name='extension', lookup_expr='iexact')
    
    class Meta:
        model = BucketFile
        fields = {
            'key': ['icontains'],
            'size': ['exact', 'lt', 'gt'],
            'last_modified': ['exact', 'lt', 'gt'],
            'extension': ['exact']
        }