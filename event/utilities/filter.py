from django_filters import rest_framework as filters
from ..models import Event

class EventFilter(filters.FilterSet):
    event_type = filters.ChoiceFilter(choices=Event.TYPE_CHOICES)  # Filters by type
    registration_type = filters.ChoiceFilter(choices=Event.REGISTRATION_TYPE_CHOICES)
    registration_link = filters.BooleanFilter(method='filter_registration_link')  # Filters by registration link existence
    is_featured_event = filters.BooleanFilter()  # Filters by featured status
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category__id')  # Filter by category ID
    
    organizer_name = filters.CharFilter(field_name='organizer__name', lookup_expr='icontains')
    organizer_id = filters.NumberFilter(field_name='organizer__id')  # Filter by organizer ID
    
    created_date = filters.DateFilter(field_name="created_date", lookup_expr="exact")
    created_date__gte = filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = filters.DateFilter(field_name="created_date", lookup_expr="lte")
    
    updated_date = filters.DateFilter(field_name="updated_date", lookup_expr="exact")
    updated_date__gte = filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = filters.DateFilter(field_name="updated_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ['event_type', 'registration_link', 'is_featured_event', 'category','organizer','registration_type','created_date','created_date__gte','created_date__lte','updated_date','updated_date__gte','updated_date__lte']

    def filter_registration_link(self, queryset, name, value):
        """
        Custom filter to check if registration_link is present or not.
        True: registration_link is not null or empty.
        False: registration_link is null or empty.
        """
        if value:
            return queryset.exclude(registration_link__isnull=True).exclude(registration_link__exact='')
        return queryset.filter(registration_link__isnull=True) | queryset.filter(registration_link__exact='')
