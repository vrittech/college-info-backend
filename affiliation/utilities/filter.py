import django_filters
from django.db.models import Q
from ..models import Affiliation
from coursemanagement.models import Course
from certification.models import Certification

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class AffiliationFilter(django_filters.FilterSet):
    id = django_filters.UUIDFilter(field_name="public_id", lookup_expr="exact")

    # Support multiple values using `in` lookup
    name = CharInFilter(field_name="name", lookup_expr="in")
    address = CharInFilter(field_name="address", lookup_expr="in")
    district = CharInFilter(field_name="district__name", lookup_expr="in")
    university_type = CharInFilter(field_name="university_type", lookup_expr="in")

    # Filtering by multiple certifications (comma-separated values)
    certification = django_filters.CharFilter(method="filter_by_certifications")

    # Date and year range filters
    created_date = django_filters.DateFilter(field_name="created_date", lookup_expr="exact")
    created_date__gte = django_filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = django_filters.DateFilter(field_name="created_date", lookup_expr="lte")
    established_year = NumberInFilter(field_name="established_year", lookup_expr="in")
    established_year__gte = django_filters.NumberFilter(field_name="established_year", lookup_expr="gte")
    established_year__lte = django_filters.NumberFilter(field_name="established_year", lookup_expr="lte")
    updated_date = django_filters.DateTimeFilter(field_name="updated_date", lookup_expr="exact")
    updated_date__gte = django_filters.DateTimeFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = django_filters.DateTimeFilter(field_name="updated_date", lookup_expr="lte")

    phone_number = CharInFilter(field_name="phone_number", lookup_expr="in")
    email = CharInFilter(field_name="email", lookup_expr="in")
    description = CharInFilter(field_name="description", lookup_expr="in")
    is_verified = django_filters.BooleanFilter(field_name="is_verified")

    # ManyToMany fields filtering using custom function
    courses = django_filters.CharFilter(method="filter_by_courses")
    affiliated_colleges = django_filters.CharFilter(method="filter_by_affiliated_colleges")

    # Custom filtering methods for ManyToMany fields (comma-separated values)
    def filter_by_certifications(self, queryset, name, value):
        """Filter by multiple certifications using comma-separated values"""
        if value:
            certifications = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(certification__id__in=certifications).distinct()
        return queryset

    def filter_by_courses(self, queryset, name, value):
        """Filter by multiple courses using comma-separated values"""
        if value:
            course_ids = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(course__id__in=course_ids).distinct()
        return queryset

    def filter_by_affiliated_colleges(self, queryset, name, value):
        """Filter by multiple affiliated colleges using comma-separated values"""
        if value:
            college_ids = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(affiliatedcollege__id__in=college_ids).distinct()
        return queryset

    class Meta:
        model = Affiliation
        fields = [
            "id", "name", "address", "district", "university_type",
            "certification", "created_date", "established_year",
            "updated_date", "phone_number", "email", "description",
            "is_verified", "courses", "affiliated_colleges"
        ]
