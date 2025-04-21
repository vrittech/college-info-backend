from django_filters import rest_framework as filters
from ..models import Event

# Custom InFilter to support filtering with multiple values
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class EventFilter(filters.FilterSet):
    event_type = CharInFilter(field_name='event_type', lookup_expr='in')  # Multi-choice
    registration_type = CharInFilter(field_name='registration_type', lookup_expr='in')
    
    registration_link = filters.BooleanFilter(method='filter_registration_link')
    is_featured_event = filters.BooleanFilter()
    is_expired = filters.BooleanFilter()
    
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    category_id = NumberInFilter(field_name='category__id', lookup_expr='in')  # Accepts multiple IDs
    
    organizer_name = filters.CharFilter(field_name='organizer__name', lookup_expr='icontains')
    organizer_id = NumberInFilter(field_name='organizer__id', lookup_expr='in')
    
    created_date = filters.DateFilter(field_name="created_date", lookup_expr="exact")
    created_date__gte = filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = filters.DateFilter(field_name="created_date", lookup_expr="lte")
    
    updated_date = filters.DateFilter(field_name="updated_date", lookup_expr="exact")
    updated_date__gte = filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = filters.DateFilter(field_name="updated_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = [
            'event_type', 'registration_link','is_expired', 'is_featured_event',
            'category_name', 'category_id', 'organizer_name', 'organizer_id',
            'registration_type', 'created_date', 'created_date__gte', 'created_date__lte',
            'updated_date', 'updated_date__gte', 'updated_date__lte',
        ]

    def filter_registration_link(self, queryset, name, value):
        if value:
            return queryset.exclude(registration_link__isnull=True).exclude(registration_link__exact='')
        return queryset.filter(registration_link__isnull=True) | queryset.filter(registration_link__exact='')
