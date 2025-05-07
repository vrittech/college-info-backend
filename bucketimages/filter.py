
from django_filters import FilterSet, DateFilter, CharFilter
class BucketFileFilter(FilterSet):
    date = DateFilter(field_name='last_modified', lookup_expr='exact')
    start_date = DateFilter(field_name='last_modified', lookup_expr='gte')
    end_date = DateFilter(field_name='last_modified', lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = None  # We'll set this dynamically
        fields = ['name', 'start_date', 'end_date','date']