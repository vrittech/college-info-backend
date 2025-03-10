import django_filters
from ..models import Information

class InformationFilter(django_filters.FilterSet):
    """
    Filter class for searching Information by multiple keys and values.
    Allows filtering by comma-separated IDs for Many-to-Many fields.
    """

    level = django_filters.BaseInFilter(field_name="level__id", lookup_expr="in")
    sublevel = django_filters.BaseInFilter(field_name="sublevel__id", lookup_expr="in")
    course = django_filters.BaseInFilter(field_name="course__id", lookup_expr="in")
    affiliation = django_filters.BaseInFilter(field_name="affiliation__id", lookup_expr="in")
    university_type = django_filters.CharFilter(method="filter_by_university_type")
    district = django_filters.BaseInFilter(field_name="district__id", lookup_expr="in")
    college = django_filters.BaseInFilter(field_name="college__id", lookup_expr="in")
    faculty = django_filters.BaseInFilter(field_name="faculty__id", lookup_expr="in")
    information_tagging = django_filters.BaseInFilter(field_name="information_tagging__id", lookup_expr="in")
    information_category = django_filters.BaseInFilter(field_name="information_category__id", lookup_expr="in")
    information_category_slug = django_filters.BaseInFilter(field_name="information_category__slug", lookup_expr="in")
    
    publish_date = django_filters.DateFromToRangeFilter(field_name="publish_date")
    active_period_start = django_filters.DateFromToRangeFilter(field_name="active_period_start")
    active_period_end = django_filters.DateFromToRangeFilter(field_name="active_period_end")

    class Meta:
        model = Information
        fields = ['level', 'sublevel', 'course', 'affiliation', 'district', 'college',
                  'faculty', 'information_tagging', 'information_category','information_category_slug',
                  'publish_date', 'active_period_start', 'active_period_end',"university_type"]
        
        
    def filter_by_university_type(self, queryset, name, value):
        """Filter by university type in Affiliation model"""
        return queryset.filter(affiliation__university_type__icontains=value).distinct()
