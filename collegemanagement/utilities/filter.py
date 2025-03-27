import django_filters
from django.db.models import Q
from ..models import College
from district.models import District
from affiliation.models import Affiliation
from collegetype.models import CollegeType
from discipline.models import Discipline
from facilities.models import Facility


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class CollegeFilter(django_filters.FilterSet):
    id = django_filters.UUIDFilter(field_name="public_id", lookup_expr="exact")

    # Support multiple values using `in` lookup
    name = CharInFilter(field_name="name", lookup_expr="in")
    address = CharInFilter(field_name="address", lookup_expr="in")
    district = CharInFilter(field_name="district__name", lookup_expr="in")
    college_type = django_filters.CharFilter(field_name="college_type__id", lookup_expr="exact")
    affiliated = django_filters.CharFilter(method="filter_by_affiliation")
    affiliated_slug = django_filters.CharFilter(method="filter_by_affiliation_slug")
    university_type = django_filters.CharFilter(field_name='affiliated__university_type', lookup_expr='icontains')
    courses = django_filters.CharFilter(method="filter_by_courses")


    # Date and year range filters
    established_date = django_filters.DateFilter(field_name="established_date", lookup_expr="exact")
    established_date__gte = django_filters.DateFilter(field_name="established_date", lookup_expr="gte")
    established_date__lte = django_filters.DateFilter(field_name="established_date", lookup_expr="lte")
    
    created_date = django_filters.DateFilter(field_name="created_date", lookup_expr="exact")
    created_date__gte = django_filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = django_filters.DateFilter(field_name="created_date", lookup_expr="lte")
    
    updated_date = django_filters.DateFilter(field_name="updated_date", lookup_expr="exact")
    updated_date__gte = django_filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = django_filters.DateFilter(field_name="updated_date", lookup_expr="lte")

    phone_number = CharInFilter(field_name="phone_number", lookup_expr="in")
    email = CharInFilter(field_name="email", lookup_expr="in")
    is_show = django_filters.BooleanFilter(field_name="is_show")
    is_verified = django_filters.BooleanFilter(field_name="is_show")

    # ManyToMany fields filtering using comma-separated values
    discipline = django_filters.CharFilter(method="filter_by_disciplines")
    facilities = django_filters.CharFilter(method="filter_by_facilities")

    # Custom filtering methods for ManyToMany fields (comma-separated values)
    def filter_by_disciplines(self, queryset, name, value):
        """Filter by multiple disciplines using comma-separated values"""
        if value:
            discipline_ids = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(discipline__id__in=discipline_ids).distinct()
        return queryset

    def filter_by_facilities(self, queryset, name, value):
        """Filter by multiple facilities using comma-separated values"""
        if value:
            facility_ids = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(college_facilities__id__in=facility_ids).distinct()
        return queryset
    
    def filter_by_courses(self, queryset, name, value):
        """Filter by multiple facilities using comma-separated values"""
        if value:
            course_ids = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(college_courses_and_fees__course__id__in=course_ids).distinct()
        return queryset
    
    def filter_by_affiliation(self, queryset, name, value):
        """Filter by multiple facilities using comma-separated values"""
        if value:
            affiliated_ids = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(affiliated__id__in=affiliated_ids).distinct()
        return queryset
    
    def filter_by_affiliation_slug(self, queryset, name, value):
        """Filter by multiple facilities using comma-separated values"""
        if value:
            affiliated_slug = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(affiliated__slug__in=affiliated_slug).distinct()
        return queryset

    class Meta:
        model = College
        fields = [
            "id", "name", "address", "district", "college_type", "affiliated",
            "established_date", "created_date", "updated_date", 'is_verified',
            "phone_number", "email", "is_show", "discipline", "college_facilities","university_type","courses","affiliated_slug"
        ]
