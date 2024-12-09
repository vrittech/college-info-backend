from django_filters import rest_framework as filters
from ..models import Event

class EventFilter(filters.FilterSet):
    event_type = filters.ChoiceFilter(choices=Event.TYPE_CHOICES)  # Filters by type
    registration_link = filters.BooleanFilter(method='filter_registration_link')  # Filters by registration link existence
    is_featured_event = filters.BooleanFilter()  # Filters by featured status
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')  # Filters by category name (many-to-many)

    class Meta:
        model = Event
        fields = ['event_type', 'registration_link', 'is_featured_event', 'category']

    def filter_registration_link(self, queryset, name, value):
        """
        Custom filter to check if registration_link is present or not.
        True: registration_link is not null or empty.
        False: registration_link is null or empty.
        """
        if value:
            return queryset.exclude(registration_link__isnull=True).exclude(registration_link__exact='')
        return queryset.filter(registration_link__isnull=True) | queryset.filter(registration_link__exact='')
