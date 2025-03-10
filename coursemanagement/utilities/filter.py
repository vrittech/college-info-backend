import django_filters
from django_filters import rest_framework as filters
from ..models import Course

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class CourseFilter(filters.FilterSet):
    id = NumberInFilter(field_name='id', lookup_expr='in')
    name = CharInFilter(field_name='name', lookup_expr='in')
    abbreviation = CharInFilter(field_name='abbreviation', lookup_expr='in')
    duration = NumberInFilter(field_name='duration__id', lookup_expr='in')
    faculty = NumberInFilter(field_name='faculty__id', lookup_expr='in')
    level = NumberInFilter(field_name='level__id', lookup_expr='in')
    affiliation = NumberInFilter(field_name='affiliation__id', lookup_expr='in')
    university_type = django_filters.CharFilter(field_name='affiliation__university_type', lookup_expr='icontains')
    description = CharInFilter(field_name='description', lookup_expr='in')
    course_shortdescription = CharInFilter(field_name='course_shortdescription', lookup_expr='in')
    course_outcome = CharInFilter(field_name='course_outcome', lookup_expr='in')
    eligibility_criteria = CharInFilter(field_name='eligibility_criteria', lookup_expr='in')
    created_date = django_filters.DateFilter(field_name="created_date", lookup_expr="exact")
    created_date__gte = django_filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = django_filters.DateFilter(field_name="created_date", lookup_expr="lte")
    
    updated_date = django_filters.DateFilter(field_name="updated_date", lookup_expr="exact")
    updated_date__gte = django_filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = django_filters.DateFilter(field_name="updated_date", lookup_expr="lte")

    discipline = django_filters.CharFilter(method='filter_by_disciplines')

    def filter_by_disciplines(self, queryset, name, value):
        if value:
            disciplines = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(discipline__id__in=disciplines).distinct()
        return queryset

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'abbreviation', 'duration', 'faculty', 'level',
            'affiliation', 'description', 'discipline', 'course_shortdescription',
            'course_outcome', 'eligibility_criteria', 'created_date', 'updated_date','university_type'
        ]