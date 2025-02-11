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
    description = CharInFilter(field_name='description', lookup_expr='in')
    course_shortdescription = CharInFilter(field_name='course_shortdescription', lookup_expr='in')
    course_outcome = CharInFilter(field_name='course_outcome', lookup_expr='in')
    eligibility_criteria = CharInFilter(field_name='eligibility_criteria', lookup_expr='in')
    created_date = filters.DateFromToRangeFilter(field_name='created_date')
    updated_date = filters.DateTimeFromToRangeFilter(field_name='updated_date')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'abbreviation', 'duration', 'faculty', 'level',
            'affiliation', 'description', 'course_shortdescription', 
            'course_outcome', 'eligibility_criteria', 'created_date', 'updated_date'
        ]
